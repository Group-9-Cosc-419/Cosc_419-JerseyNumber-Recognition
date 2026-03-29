"""
inference_multitask.py — COSC 419 Multi-Task Jersey Number Inference
Group 9

Replaces PARSeq (str.py) in the pipeline's Stage 7.
Outputs jersey_id_results.json in the EXACT format PARSeq produces:

    {
        "0_1.jpg": {
            "label": "4",
            "confidence": [0.999, 0.999],
        },
        "0_2.jpg": { ... },
        ...
    }

Keys are flat image filenames (e.g., "260_513.jpg"), NOT nested by tracklet.

Usage:
    python inference_multitask.py \
        --checkpoint best_multitask_resnet34.pth \
        --data_root out/SoccerNetResults/test/crops \
        --result_file out/SoccerNetResults/jersey_id_results.json \
        --theta 0.5
"""

from __future__ import annotations

import argparse
import json
import os

import torch
from torch.nn import functional as F
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
from tqdm import tqdm

from recognition_multitask import MultiTaskSTRRecognizer

TENS_NULL = 10


class CropDataset(Dataset):
    """Simple dataset that loads all crop images from tracklet subdirectories."""

    def __init__(self, data_root: str):
        self.transform = transforms.Compose([
            transforms.Resize((32, 128)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

        self.samples = []  # (full_path, filename_key)
        for tracklet_id in sorted(os.listdir(data_root)):
            tracklet_dir = os.path.join(data_root, tracklet_id)
            if not os.path.isdir(tracklet_dir) or tracklet_id.startswith('.'):
                continue
            for fname in sorted(os.listdir(tracklet_dir)):
                if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
                    continue
                if fname.startswith('.'):
                    continue
                full_path = os.path.join(tracklet_dir, fname)
                # Key format matches PARSeq: "tracklet_frame.jpg"
                self.samples.append((full_path, fname))

        print(f"Loaded {len(self.samples)} crop images")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, key = self.samples[idx]
        image = Image.open(path).convert('RGB')
        image = self.transform(image)
        return image, key


def run_inference(
    model: MultiTaskSTRRecognizer,
    data_root: str,
    device: torch.device,
    theta: float = 0.5,
    batch_size: int = 64,
    num_workers: int = 2,
) -> dict:
    """Run batched inference on all crops."""

    dataset = CropDataset(data_root)
    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=torch.cuda.is_available(),
    )

    results = {}
    full_head_used = 0
    digit_head_used = 0

    model.eval()
    with torch.no_grad():
        for images, keys in tqdm(dataloader, desc="Inference"):
            images = images.to(device)
            out_full, out_tens, out_ones = model(images)

            probs_full = F.softmax(out_full, dim=1)
            probs_tens = F.softmax(out_tens, dim=1)
            probs_ones = F.softmax(out_ones, dim=1)

            conf_full, pred_full = probs_full.max(dim=1)
            conf_tens, pred_tens = probs_tens.max(dim=1)
            conf_ones, pred_ones = probs_ones.max(dim=1)

            for i, key in enumerate(keys):
                cf = conf_full[i].item()
                pf = pred_full[i].item()
                ct = conf_tens[i].item()
                pt = pred_tens[i].item()
                co = conf_ones[i].item()
                po = pred_ones[i].item()

                # θ threshold logic
                if cf >= theta:
                    prediction = pf
                    confidence = [cf]
                    full_head_used += 1
                else:
                    if pt == TENS_NULL:
                        prediction = po
                        confidence = [co]
                    else:
                        prediction = pt * 10 + po
                        confidence = [ct, co]
                    digit_head_used += 1

                # Match PARSeq output format exactly
                results[key] = {
                    "label": str(int(prediction)),
                    "confidence": confidence,
                }

    total = full_head_used + digit_head_used
    print(f"\nInference complete: {total} images")
    print(f"  Full head used: {full_head_used} ({100*full_head_used/max(total,1):.1f}%)")
    print(f"  Digit heads used: {digit_head_used} ({100*digit_head_used/max(total,1):.1f}%)")

    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--data_root", type=str, required=True)
    parser.add_argument("--result_file", type=str, default="jersey_id_results.json")
    parser.add_argument("--theta", type=float, default=0.5)
    parser.add_argument("--batch_size", type=int, default=64)
    parser.add_argument("--num_workers", type=int, default=2)
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    model = MultiTaskSTRRecognizer(pretrained=False)
    state_dict = torch.load(args.checkpoint, map_location=device, weights_only=False)
    model.load_state_dict(state_dict)
    model.to(device)
    print(f"Loaded checkpoint: {args.checkpoint}")

    results = run_inference(
        model, args.data_root, device,
        theta=args.theta,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
    )

    with open(args.result_file, 'w') as f:
        json.dump(results, f)
    print(f"Saved {len(results)} predictions to {args.result_file}")


if __name__ == "__main__":
    main()
