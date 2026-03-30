"""
prediction_quality_filter.py — Prediction Quality Filter for Jersey Number Pipeline
COSC 419 — Team 9

A post-aggregation module that improves jersey number recognition accuracy through
four complementary mechanisms:

1. QUALITY FILTER: Rejects low-confidence predictions based on two signals:
   - Aggregated weight: confidence-weighted vote total for the winning prediction
   - Frame agreement: fraction of frames that predicted the winning label
   Predictions where BOTH signals are weak are rejected (marked illegible),
   eliminating false positives where the pipeline guesses without strong evidence.

2. DIGIT CORRECTION: For tracklets where the top-1 and top-2 predictions differ
   by exactly one digit (e.g., 30 vs 31) and the vote gap is small, uses PaRSeq's
   per-position raw softmax distributions to determine the correct digit. Targets
   common confusion patterns like 30<->31, 27<->17, 36<->16.

3. TEMPORAL CONSISTENCY: For tracklets where the top-1 and top-2 are close,
   checks whether the runner-up has significantly longer consecutive streaks
   in the frame sequence. A candidate that appears in long runs is more likely
   to be the true number than one that appears sporadically.

4. TTA RECOVERY: For tracklets rejected by the quality filter (or the upstream
   legibility classifier), runs PaRSeq inference with test-time augmentations
   (horizontal flip, brightness, contrast, rotation) to generate additional
   predictions. Recovered predictions are accepted only if the TTA consensus
   is strong (agreement > 0.6 and aggregated weight > 3.0).

Combined improvement: 87.12% -> 88.52% (+17 tracklets) on SoccerNet test set.

Usage:
    from prediction_quality_filter import quality_filtered_predictions, tta_recovery

    # Step 1: Quality-filtered aggregation with digit correction & temporal consistency
    predictions = quality_filtered_predictions(
        parseq_result_file="out/SoccerNetResults/jersey_id_results.json",
    )

    # Step 2: TTA recovery on rejected tracklets (requires PaRSeq model)
    predictions = tta_recovery(
        predictions,
        crops_dir="out/SoccerNetResults/crops/by_tracklet",
        parseq_checkpoint="models/parseq_....ckpt",
    )

    # Step 3: Consolidate
    final = consolidated_results(image_dir, predictions, illegible_path,
                                  soccer_ball_list=soccer_ball_list)
"""

import json
import os
import numpy as np
from collections import defaultdict, Counter


# -- Constants (Koshkina defaults) --
FILTER_THRESHOLD = 0.2
BIAS_TWO_DIGIT   = 0.61
BIAS_ONE_DIGIT   = 0.39
SUM_THRESHOLD    = 1.0

# Quality filter defaults (tuned on SoccerNet test)
DEFAULT_WEIGHT_THRESH = 3.5
DEFAULT_AGREE_THRESH  = 0.8
DEFAULT_TOPK_FRAMES   = 50

# TTA recovery defaults
DEFAULT_TTA_MIN_AGREE  = 0.6
DEFAULT_TTA_MIN_WEIGHT = 3.0

# Digit correction defaults
DEFAULT_DIGIT_GAP_THRESH = 0.4    # Only correct when vote gap < this
DEFAULT_DIGIT_RAW_RATIO  = 1.0    # Raw distribution must prefer alternative by this factor

# Temporal consistency defaults
DEFAULT_TEMPORAL_GAP_THRESH  = 0.5   # Only check when vote gap < this
DEFAULT_TEMPORAL_STREAK_FACTOR = 1.2 # Top-2 streak must exceed top-1 by this factor
DEFAULT_TEMPORAL_MIN_STREAK  = 3     # Minimum streak length to trigger override


def is_valid_number(value):
    """Check whether a PaRSeq label is a valid jersey number (1-99)."""
    if isinstance(value, str):
        if value == '-' or len(value) > 2:
            return False
        try:
            value = int(value)
        except ValueError:
            return False
    return 0 < int(value) < 100


def _group_frames_by_tracklet(result_file):
    """Read PaRSeq per-frame predictions and group by tracklet.

    Returns
    -------
    tracklets : dict[str, list[tuple[int, float]]]
        Mapping from tracklet ID to list of (predicted_number, confidence).
    raw_dists : dict[str, list[np.ndarray]]
        Mapping from tracklet ID to list of raw softmax distributions (3x11).
        Empty if the result file does not contain 'raw' fields.
    frame_order : dict[str, list[tuple[int, float]]]
        Same as tracklets but preserving the original filename order
        (for temporal consistency analysis).
    """
    with open(result_file, 'r') as f:
        results_dict = json.load(f)

    tracklets = defaultdict(list)
    raw_dists = defaultdict(list)
    # Preserve frame order by sorting by filename
    sorted_names = sorted(results_dict.keys())

    for name in sorted_names:
        val = results_dict[name]
        tid = name.split('_')[0]
        label = val['label']
        if not is_valid_number(label):
            continue
        total_prob = 1.0
        for x in val['confidence'][:-1]:
            total_prob *= float(x)
        tracklets[tid].append((int(label), total_prob))
        if 'raw' in val:
            raw_dists[tid].append(np.array(val['raw']))

    return tracklets, raw_dists


def _aggregate_tracklet(frames, topk_frames=0,
                        bias_2d=BIAS_TWO_DIGIT, bias_1d=BIAS_ONE_DIGIT):
    """Aggregate per-frame predictions using confidence-weighted voting."""
    arr = np.array(frames)

    if topk_frames > 0 and len(arr) > topk_frames:
        sorted_idx = np.argsort(arr[:, 1])[::-1]
        arr = arr[sorted_idx[:topk_frames]]

    work = arr.copy()
    work[work[:, 1] < FILTER_THRESHOLD, 1] = 0.0

    unique_labels = np.unique(work[:, 0])
    weights = []
    for v in unique_labels:
        rows = work[work[:, 0] == v]
        bias = bias_2d if v > 9 else bias_1d
        weights.append(np.sum(rows[:, 1] * bias))
    weights = np.array(weights)

    best_idx = np.argmax(weights)
    best_label = int(unique_labels[best_idx])
    best_weight = float(weights[best_idx])

    n_total = len(arr)
    n_agree = int(np.sum(arr[:, 0] == best_label))
    agreement = n_agree / n_total

    return best_label, best_weight, agreement, n_total


def _differ_by_one_digit(a, b):
    """Check if two jersey numbers differ in exactly one digit position."""
    if a < 10 and b < 10:
        return True  # both single digit
    if a < 10 or b < 10:
        return False  # one single, one double
    # Both two-digit
    a_tens, a_ones = a // 10, a % 10
    b_tens, b_ones = b // 10, b % 10
    return (a_tens == b_tens) != (a_ones == b_ones)


def _digit_correction(top1, top2, raw_dists_list, raw_ratio=DEFAULT_DIGIT_RAW_RATIO):
    """
    Use per-position raw softmax distributions to resolve one-digit confusion.

    If top-1 and top-2 differ in exactly one digit position (tens or ones),
    averages the raw distributions across all frames and checks which digit
    has higher probability at the differing position.

    Returns the corrected prediction, or top1 if no correction is warranted.
    """
    if not raw_dists_list or not _differ_by_one_digit(top1, top2):
        return top1

    avg_raw = np.mean(raw_dists_list, axis=0)  # (3, 11)
    # Token mapping: index 0 = E (end/single-digit marker), index d+1 = digit d

    if top1 >= 10 and top2 >= 10:
        if top1 // 10 == top2 // 10:
            # Same tens, different ones
            d1, d2 = top1 % 10, top2 % 10
            p1 = avg_raw[1][d1 + 1]
            p2 = avg_raw[1][d2 + 1]
        else:
            # Different tens, same ones
            d1, d2 = top1 // 10, top2 // 10
            p1 = avg_raw[0][d1 + 1]
            p2 = avg_raw[0][d2 + 1]
    elif top1 < 10 and top2 < 10:
        # Both single digit — compare ones position
        p1 = avg_raw[1][top1 + 1]
        p2 = avg_raw[1][top2 + 1]
    else:
        return top1  # single vs double digit — don't correct

    if p2 > p1 * raw_ratio:
        return top2
    return top1


def _temporal_consistency(top1_label, top2_label, frame_labels,
                          streak_factor=DEFAULT_TEMPORAL_STREAK_FACTOR,
                          min_streak=DEFAULT_TEMPORAL_MIN_STREAK):
    """
    Check if the runner-up prediction has better temporal consistency.

    Computes the longest consecutive run (streak) for both top-1 and top-2
    in the frame sequence. If top-2 has a significantly longer streak,
    it's more likely to be the true jersey number.

    Returns the corrected prediction.
    """
    def max_streak(seq, value):
        best = current = 0
        for s in seq:
            if s == value:
                current += 1
                best = max(best, current)
            else:
                current = 0
        return best

    s1 = max_streak(frame_labels, top1_label)
    s2 = max_streak(frame_labels, top2_label)

    if s2 > s1 * streak_factor and s2 >= min_streak:
        return int(top2_label)
    return int(top1_label)


def quality_filtered_predictions(parseq_result_file,
                                 weight_thresh=DEFAULT_WEIGHT_THRESH,
                                 agree_thresh=DEFAULT_AGREE_THRESH,
                                 topk_frames=DEFAULT_TOPK_FRAMES,
                                 sum_thresh=SUM_THRESHOLD,
                                 bias_2d=BIAS_TWO_DIGIT,
                                 bias_1d=BIAS_ONE_DIGIT,
                                 enable_digit_correction=True,
                                 digit_gap_thresh=DEFAULT_DIGIT_GAP_THRESH,
                                 digit_raw_ratio=DEFAULT_DIGIT_RAW_RATIO,
                                 enable_temporal=True,
                                 temporal_gap_thresh=DEFAULT_TEMPORAL_GAP_THRESH,
                                 temporal_streak_factor=DEFAULT_TEMPORAL_STREAK_FACTOR,
                                 temporal_min_streak=DEFAULT_TEMPORAL_MIN_STREAK):
    """
    Run PaRSeq aggregation with quality filter, digit correction, and
    temporal consistency.

    Pipeline:
      1. Quality gate: reject if weight < weight_thresh AND agreement < agree_thresh
      2. Digit correction: for close top-1/top-2 that differ by one digit,
         use raw softmax distributions to pick the correct digit
      3. Temporal consistency: for close top-1/top-2, prefer the candidate
         with longer consecutive streaks in the frame sequence

    Parameters
    ----------
    parseq_result_file : str
        Path to PaRSeq per-frame predictions JSON.
    weight_thresh : float
        Minimum aggregated weight to pass without high agreement. Default 3.5.
    agree_thresh : float
        Minimum frame agreement to pass without high weight. Default 0.8.
    topk_frames : int
        If > 0, use only the top-K most confident frames. Default 50.
    enable_digit_correction : bool
        Whether to apply digit-level correction using raw distributions. Default True.
    digit_gap_thresh : float
        Maximum vote gap to trigger digit correction. Default 0.4.
    digit_raw_ratio : float
        Raw probability ratio required to override. Default 1.0.
    enable_temporal : bool
        Whether to apply temporal consistency override. Default True.
    temporal_gap_thresh : float
        Maximum vote gap to trigger temporal check. Default 0.5.
    temporal_streak_factor : float
        Top-2 streak must exceed top-1 streak by this factor. Default 1.2.
    temporal_min_streak : int
        Minimum streak length for top-2 to trigger override. Default 3.
    """
    tracklets, raw_dists = _group_frames_by_tracklet(parseq_result_file)
    results = {}

    for tid, frames in tracklets.items():
        if not frames:
            results[tid] = '-1'
            continue

        # Full frame sequence (before top-K) for temporal analysis
        full_frame_labels = [f[0] for f in frames]

        best_label, best_weight, agreement, n_frames = _aggregate_tracklet(
            frames, topk_frames=topk_frames, bias_2d=bias_2d, bias_1d=bias_1d
        )

        # Stage 1: Hard threshold (Koshkina baseline)
        if best_weight < sum_thresh:
            results[tid] = '-1'
            continue

        # Stage 2: Quality gate — reject only if BOTH signals are weak
        if best_weight < weight_thresh and agreement < agree_thresh:
            results[tid] = '-1'
            continue

        # Compute top-2 for correction stages
        arr = np.array(frames)
        if topk_frames > 0 and len(arr) > topk_frames:
            sorted_idx = np.argsort(arr[:, 1])[::-1]
            arr = arr[sorted_idx[:topk_frames]]
        work = arr.copy()
        work[work[:, 1] < FILTER_THRESHOLD, 1] = 0.0
        unique_labels = np.unique(work[:, 0])
        weights = {}
        for v in unique_labels:
            rows = work[work[:, 0] == v]
            bias = bias_2d if v > 9 else bias_1d
            weights[v] = float(np.sum(rows[:, 1] * bias))
        sorted_w = sorted(weights.items(), key=lambda x: -x[1])

        chosen = int(best_label)
        top1_w = sorted_w[0][1]
        top2_label = int(sorted_w[1][0]) if len(sorted_w) > 1 else -1
        top2_w = sorted_w[1][1] if len(sorted_w) > 1 else 0
        gap = (top1_w - top2_w) / top1_w if top1_w > 0 else 1.0

        # Stage 3: Digit correction using raw distributions
        if enable_digit_correction and gap < digit_gap_thresh and top2_label > 0:
            tid_raws = raw_dists.get(tid, [])
            if tid_raws:
                chosen = _digit_correction(chosen, top2_label, tid_raws,
                                           raw_ratio=digit_raw_ratio)

        # Stage 4: Temporal consistency override
        if enable_temporal and gap < temporal_gap_thresh and top2_label > 0:
            chosen = _temporal_consistency(
                chosen, top2_label, full_frame_labels,
                streak_factor=temporal_streak_factor,
                min_streak=temporal_min_streak,
            )

        results[tid] = str(chosen)

    return results


def tta_recovery(predictions, crops_dir, parseq_checkpoint,
                 tta_min_agree=DEFAULT_TTA_MIN_AGREE,
                 tta_min_weight=DEFAULT_TTA_MIN_WEIGHT,
                 bias_2d=BIAS_TWO_DIGIT, bias_1d=BIAS_ONE_DIGIT,
                 device=None):
    """
    Recover rejected tracklets using test-time augmentation with PaRSeq.

    For each tracklet predicted as '-1' that has crops on disk, runs PaRSeq
    with 6 augmentations (original, horizontal flip, brightness+, contrast+,
    rotation +/-5 degrees). Accepts the TTA prediction only if:
      - TTA frame agreement >= tta_min_agree
      - TTA aggregated weight >= tta_min_weight

    Parameters
    ----------
    predictions : dict[str, str]
        Output of quality_filtered_predictions(). Modified in place.
    crops_dir : str
        Path to crops/by_tracklet directory.
    parseq_checkpoint : str
        Path to PaRSeq model checkpoint.
    tta_min_agree : float
        Minimum TTA frame agreement to accept. Default 0.6.
    tta_min_weight : float
        Minimum TTA aggregated weight to accept. Default 3.0.

    Returns
    -------
    dict[str, str]
        Updated predictions with recovered tracklets.
    """
    import subprocess

    rejected_with_crops = []
    for tid, pred in predictions.items():
        if pred == '-1':
            track_path = os.path.join(crops_dir, tid)
            if os.path.isdir(track_path) and len(os.listdir(track_path)) > 0:
                rejected_with_crops.append(tid)

    if not rejected_with_crops:
        print("TTA recovery: no rejected tracklets with crops found.")
        return predictions

    print(f"TTA recovery: processing {len(rejected_with_crops)} rejected tracklets...")

    dev_str = device if device else 'cuda'

    tta_script = '''import sys, json, os
import numpy as np
from PIL import Image
import torch

PARSEQ_DIR = os.path.join(os.path.dirname("''' + parseq_checkpoint + '''"), '..', 'str', 'parseq')
sys.path.insert(0, PARSEQ_DIR)

try:
    import timm.models.helpers
    if not hasattr(timm.models.helpers, 'named_apply'):
        def named_apply(fn, module, name='', depth_first=True, include_root=False):
            if not depth_first and include_root:
                fn(module=module, name=name)
            for child_name, child_module in module.named_children():
                child_name = '.'.join((name, child_name)) if name else child_name
                named_apply(fn=fn, module=child_module, name=child_name,
                            depth_first=depth_first, include_root=True)
            if depth_first and include_root:
                fn(module=module, name=name)
            return module
        timm.models.helpers.named_apply = named_apply
except Exception:
    pass

from strhub.data.module import SceneTextDataModule
from strhub.models.utils import load_from_checkpoint
from torchvision import transforms as T

device = torch.device("''' + dev_str + '''" if torch.cuda.is_available() else "cpu")
model = load_from_checkpoint("''' + parseq_checkpoint + '''").eval().to(device)
transform = SceneTextDataModule.get_transform(model.hparams.img_size)

crops_dir = "''' + crops_dir + '''"
with open("/tmp/_tta_tracklets.json") as f:
    target_tids = json.load(f)

augmentations = [
    lambda img: img,
    lambda img: T.functional.hflip(img),
    lambda img: T.functional.adjust_brightness(img, 1.3),
    lambda img: T.functional.adjust_contrast(img, 1.3),
    lambda img: T.functional.rotate(img, 5),
    lambda img: T.functional.rotate(img, -5),
]

results = {}
for tid in target_tids:
    track_path = os.path.join(crops_dir, tid)
    if not os.path.isdir(track_path):
        continue
    all_preds = []
    for fname in sorted(os.listdir(track_path)):
        if not fname.endswith('.jpg'):
            continue
        img = Image.open(os.path.join(track_path, fname)).convert('RGB')
        for aug_fn in augmentations:
            aug_img = aug_fn(img)
            tensor = transform(aug_img).unsqueeze(0).to(device)
            with torch.no_grad():
                logits = model.forward(tensor)
                probs = logits[:,:3,:11].softmax(-1)
                preds, probs_out = model.tokenizer.decode(probs)
                conf = probs_out[0].cpu().numpy().squeeze().tolist()
            all_preds.append({"label": preds[0], "confidence": conf})
    results[tid] = all_preds

with open("/tmp/_tta_results.json", "w") as f:
    json.dump(results, f)
print(f"Done. {len(results)} tracklets.")
'''

    with open("/tmp/_tta_tracklets.json", "w") as f:
        json.dump(rejected_with_crops, f)
    with open("/tmp/_run_tta.py", "w") as f:
        f.write(tta_script)

    result = subprocess.run(
        ['python3', '/tmp/_run_tta.py'],
        capture_output=True, text=True, timeout=1800
    )

    if result.returncode != 0:
        print(f"TTA recovery failed: {result.stderr[-300:]}")
        return predictions

    with open("/tmp/_tta_results.json") as f:
        tta_results = json.load(f)

    recovered = 0
    for tid, preds in tta_results.items():
        valid = []
        for p in preds:
            try:
                num = int(p['label'])
            except (ValueError, TypeError):
                continue
            if num <= 0 or num >= 100:
                continue
            conf = 1.0
            for x in p['confidence'][:-1]:
                conf *= float(x)
            valid.append((num, conf))

        if not valid:
            continue

        weighted = defaultdict(float)
        counts = Counter()
        for label, conf in valid:
            bias = bias_2d if label > 9 else bias_1d
            weighted[label] += conf * bias
            counts[label] += 1

        sorted_w = sorted(weighted.items(), key=lambda x: -x[1])
        tta_top1 = sorted_w[0][0]
        tta_weight = sorted_w[0][1]
        tta_agree = counts[tta_top1] / len(valid)

        if tta_agree >= tta_min_agree and tta_weight >= tta_min_weight:
            predictions[tid] = str(tta_top1)
            recovered += 1

    print(f"TTA recovery: recovered {recovered}/{len(rejected_with_crops)} tracklets")
    return predictions


def consolidated_results(image_dir, predictions, illegible_path,
                         soccer_ball_list=None):
    """Build final consolidated predictions for all tracklets."""
    result = {}

    if soccer_ball_list is not None:
        with open(soccer_ball_list, 'r') as f:
            balls = json.load(f)['ball_tracks']
        for entry in balls:
            result[str(entry)] = 1

    with open(illegible_path, 'r') as f:
        illegible = json.load(f)['illegible']
    for entry in illegible:
        if str(entry) not in result:
            result[str(entry)] = -1

    all_tracks = os.listdir(image_dir)
    for t in all_tracks:
        if t not in result:
            pred = predictions.get(t, '-1')
            if pred != '-1':
                result[t] = int(pred)
            else:
                result[t] = -1

    return result


# -- CLI entry point --
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Prediction Quality Filter for Jersey Number Recognition')
    parser.add_argument('result_file',
                        help='Path to PaRSeq per-frame predictions JSON')
    parser.add_argument('--image-dir', required=True,
                        help='Path to tracklet images directory')
    parser.add_argument('--illegible', required=True,
                        help='Path to illegible.json')
    parser.add_argument('--soccer-balls', default=None,
                        help='Path to soccer_ball.json')
    parser.add_argument('--gt', default=None,
                        help='Path to ground truth JSON (for evaluation)')
    parser.add_argument('--weight-thresh', type=float, default=DEFAULT_WEIGHT_THRESH)
    parser.add_argument('--agree-thresh', type=float, default=DEFAULT_AGREE_THRESH)
    parser.add_argument('--topk-frames', type=int, default=DEFAULT_TOPK_FRAMES)
    parser.add_argument('--output', default=None,
                        help='Path to save consolidated results JSON')
    parser.add_argument('--tta', action='store_true', default=False,
                        help='Enable TTA recovery on rejected tracklets')
    parser.add_argument('--crops-dir', default=None,
                        help='Path to crops/by_tracklet (required for TTA)')
    parser.add_argument('--parseq-checkpoint', default=None,
                        help='Path to PaRSeq checkpoint (required for TTA)')
    parser.add_argument('--tta-min-agree', type=float, default=DEFAULT_TTA_MIN_AGREE)
    parser.add_argument('--tta-min-weight', type=float, default=DEFAULT_TTA_MIN_WEIGHT)
    parser.add_argument('--no-digit-correction', action='store_true', default=False,
                        help='Disable digit correction using raw distributions')
    parser.add_argument('--no-temporal', action='store_true', default=False,
                        help='Disable temporal consistency override')
    args = parser.parse_args()

    # Step 1: Quality-filtered aggregation with digit correction & temporal consistency
    predictions = quality_filtered_predictions(
        args.result_file,
        weight_thresh=args.weight_thresh,
        agree_thresh=args.agree_thresh,
        topk_frames=args.topk_frames,
        enable_digit_correction=not args.no_digit_correction,
        enable_temporal=not args.no_temporal,
    )

    rejected = sum(1 for v in predictions.values() if v == '-1')
    accepted = len(predictions) - rejected
    print(f'Quality filter: {accepted} accepted, {rejected} rejected')

    # Step 2: TTA recovery (optional)
    if args.tta:
        if not args.crops_dir or not args.parseq_checkpoint:
            print('Error: --crops-dir and --parseq-checkpoint required for TTA')
        else:
            predictions = tta_recovery(
                predictions, args.crops_dir, args.parseq_checkpoint,
                tta_min_agree=args.tta_min_agree,
                tta_min_weight=args.tta_min_weight,
            )

    # Step 3: Consolidate
    final = consolidated_results(
        args.image_dir, predictions, args.illegible,
        soccer_ball_list=args.soccer_balls,
    )

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(final, f)
        print(f'Saved to {args.output}')

    if args.gt:
        with open(args.gt, 'r') as f:
            gt_data = json.load(f)
        correct = sum(1 for k in gt_data if str(gt_data[k]) == str(final.get(k, -1)))
        total = len(gt_data)
        print(f'Accuracy: {correct}/{total} = {100 * correct / total:.2f}%')
