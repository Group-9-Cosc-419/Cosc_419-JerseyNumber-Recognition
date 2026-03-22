"""
inference_multitask.py — COSC 419 Multi-Task Jersey Number Inference
Group 9

Replaces PARSeq (str.py) in the pipeline's Stage 7.
Loads the trained multi-task ResNet-34, runs inference on crop images,
and outputs jersey_id_results.json in the EXACT format the pipeline expects.

The pipeline's helpers.process_jersey_id_predictions() expects:
    {
        "tracklet_id": {
            "image_filename": [predicted_number, confidence],
            ...
        },
        ...
    }

This script also implements the θ threshold logic from the proposal:
    - If the full head confidence >= θ, use the full head prediction
    - If the full head confidence < θ, construct prediction from digit heads:
        - tens=NULL → single digit (ones prediction)
        - tens=digit → tens*10 + ones

Usage:
    python inference_multitask.py \
        --checkpoint checkpoints/best_multitask_resnet34.pth \
        --data_root out/SoccerNetResults/test/crops \
        --result_file out/SoccerNetResults/jersey_id_results.json \
        --theta 0.5
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import torch
from torch.nn import functional as F
from torchvision import transforms
from PIL import Image
from tqdm import tqdm

from recognition_multitask import MultiTaskSTRRecognizer

# ── Constants ──
TENS_NULL = 10  # Index for "no tens digit" in the tens head


def load_model(checkpoint_path: str, device: torch.device) -> MultiTaskSTRRecognizer:
    """Load trained multi-task model from checkpoint."""
    model = MultiTaskSTRRecognizer(pretrained=False)
    state_dict = torch.load(checkpoint_path, map_location=device, weights_only=False)
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()
    print(f"Loaded model from {checkpoint_path}")
    return model


def get_transform() -> transforms.Compose:
    """Same transform used during training (val/test mode)."""
    return transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])


def predict_single(
    model: MultiTaskSTRRecognizer,
    image: torch.Tensor,
    device: torch.device,
    theta: float = 0.5,
) -> tuple[int, float]:
    """
    Run inference on a single image and apply the θ threshold logic.

    Returns:
        (predicted_number, confidence)
    """
    image = image.unsqueeze(0).to(device)

    with torch.no_grad():
        out_full, out_tens, out_ones = model(image)

    # Full head prediction
    probs_full = F.softmax(out_full, dim=1)
    conf_full, pred_full = probs_full.max(dim=1)
    conf_full = conf_full.item()
    pred_full = pred_full.item()

    # Digit heads predictions
    probs_tens = F.softmax(out_tens, dim=1)
    probs_ones = F.softmax(out_ones, dim=1)
    conf_tens, pred_tens = probs_tens.max(dim=1)
    conf_ones, pred_ones = probs_ones.max(dim=1)
    pred_tens = pred_tens.item()
    pred_ones = pred_ones.item()

    # θ threshold logic (from proposal Section 3.2):
    # If full head is confident enough, use it directly.
    # Otherwise, construct from digit heads.
    if conf_full >= theta:
        return pred_full, conf_full
    else:
        # Construct from digit heads
        if pred_tens == TENS_NULL:
            # Single digit jersey
            constructed = pred_ones
        else:
            # Two digit jersey
            constructed = pred_tens * 10 + pred_ones

        # Use the average digit confidence as the overall confidence
        digit_conf = (conf_tens.item() + conf_ones.item()) / 2.0
        return constructed, digit_conf


def run_inference(
    model: MultiTaskSTRRecognizer,
    data_root: str,
    device: torch.device,
    theta: float = 0.5,
    batch_size: int = 32,
) -> dict:
    """
    Run inference on all crop images and produce jersey_id_results.json format.

    The crop directory structure is:
        data_root/
            tracklet_0/
                img1.jpg
                img2.jpg
            tracklet_1/
                ...

    Output format matches PARSeq's str.py:
        {
            "tracklet_id": {
                "image_filename": [predicted_number, confidence],
                ...
            }
        }
    """
    transform = get_transform()
    results = {}

    # Get all tracklet directories
    tracklets = sorted([
        t for t in os.listdir(data_root)
        if os.path.isdir(os.path.join(data_root, t)) and not t.startswith('.')
    ])

    print(f"Running inference on {len(tracklets)} tracklets from {data_root}")

    total_images = 0
    full_head_used = 0
    digit_head_used = 0

    for tracklet_id in tqdm(tracklets, desc="Inference"):
        tracklet_dir = os.path.join(data_root, tracklet_id)
        tracklet_results = {}

        images = sorted([
            f for f in os.listdir(tracklet_dir)
            if f.lower().endswith(('.jpg', '.jpeg', '.png')) and not f.startswith('.')
        ])

        for img_name in images:
            img_path = os.path.join(tracklet_dir, img_name)
            try:
                image = Image.open(img_path).convert('RGB')
                image_tensor = transform(image)

                pred_number, confidence = predict_single(model, image_tensor, device, theta)

                # Store as [prediction, confidence] — same format as PARSeq
                tracklet_results[img_name] = [int(pred_number), float(confidence)]
                total_images += 1

                # Track which head was used (for ablation reporting)
                # We can check by re-running the logic, but simpler to just count
                with torch.no_grad():
                    out_full, _, _ = model(image_tensor.unsqueeze(0).to(device))
                    probs_full = F.softmax(out_full, dim=1)
                    if probs_full.max().item() >= theta:
                        full_head_used += 1
                    else:
                        digit_head_used += 1

            except Exception as e:
                print(f"  Warning: failed on {img_path}: {e}")
                continue

        if tracklet_results:
            results[tracklet_id] = tracklet_results

    print(f"\nInference complete:")
    print(f"  Total images: {total_images}")
    print(f"  Full head used: {full_head_used} ({100*full_head_used/max(total_images,1):.1f}%)")
    print(f"  Digit heads used: {digit_head_used} ({100*digit_head_used/max(total_images,1):.1f}%)")
    print(f"  Tracklets with predictions: {len(results)}")

    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Multi-task jersey number inference")
    parser.add_argument("--checkpoint", type=str, required=True,
                        help="Path to trained model checkpoint (.pth)")
    parser.add_argument("--data_root", type=str, required=True,
                        help="Path to crop images directory")
    parser.add_argument("--result_file", type=str, default="jersey_id_results.json",
                        help="Output JSON path")
    parser.add_argument("--theta", type=float, default=0.5,
                        help="Confidence threshold for full head vs digit heads")
    parser.add_argument("--batch_size", type=int, default=1,
                        help="Batch size (currently processes one at a time)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    model = load_model(args.checkpoint, device)
    results = run_inference(model, args.data_root, device, theta=args.theta)

    # Save results
    with open(args.result_file, 'w') as f:
        json.dump(results, f)
    print(f"Results saved to {args.result_file}")


if __name__ == "__main__":
    main()
