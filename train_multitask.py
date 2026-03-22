"""
train_multitask.py — COSC 419 Multi-Task Jersey Number Classifier
Group 9

Trains a shared-backbone ResNet-34 with three heads:
  - Full number (100 classes: 0–99)
  - Tens digit  (11 classes: 0–9 + NULL=10)
  - Ones digit  (10 classes: 0–9)

Uses Karo/Aaditya's JerseyNumberMultitaskDataset (CSV annotations + image dir),
NOT ImageFolder. This matches SoccerNet's actual data format.

Changes from Aaditya's original:
  - Swapped ImageFolder dataset for JerseyNumberMultitaskDataset
  - Added cosine annealing LR scheduler (per proposal)
  - Added early stopping on validation accuracy (per proposal)
  - Added lambda weights for tens/ones losses (per proposal)
  - Saves best model checkpoint (not just every 5 epochs)

Usage:
  python train_multitask.py \\
      --train-annotations data/SoccerNet/train/train_gt.json \\
      --train-images data/SoccerNet/train/images \\
      --val-annotations data/SoccerNet/val/val_gt.json \\
      --val-images data/SoccerNet/val/images \\
      --epochs 50 \\
      --batch-size 32
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict

import torch
from torch import nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR
from torch.utils.data import DataLoader
from tqdm import tqdm

# ── Import from teammate files ──────────────────────────────
# recognition_multitask.py = Aaditya's shared-backbone model (recognition-2.py)
# jersey_number_dataset.py = Fixed dataset that reads SoccerNet JSON + expands tracklets to frames
from recognition_multitask import MultiTaskSTRRecognizer
from jersey_number_dataset import JerseyNumberMultitaskDataset


def train_one_epoch(
    model: nn.Module,
    dataloader: DataLoader,
    criterion: nn.Module,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
    epoch: int,
    num_epochs: int,
    lambda_tens: float = 1.0,
    lambda_ones: float = 1.0,
) -> Dict[str, float]:
    model.train()
    running = {
        "total_loss": 0.0,
        "loss_full": 0.0,
        "loss_tens": 0.0,
        "loss_ones": 0.0,
        "correct_full": 0,
        "num_samples": 0,
    }

    progress = tqdm(dataloader, desc=f"Epoch {epoch}/{num_epochs} [train]")
    for images, labels_full, labels_tens, labels_ones in progress:
        images = images.to(device, non_blocking=True)
        labels_full = labels_full.to(device, dtype=torch.long, non_blocking=True)
        labels_tens = labels_tens.to(device, dtype=torch.long, non_blocking=True)
        labels_ones = labels_ones.to(device, dtype=torch.long, non_blocking=True)

        optimizer.zero_grad(set_to_none=True)

        out_full, out_tens, out_ones = model(images)
        loss_full = criterion(out_full, labels_full)
        loss_tens = criterion(out_tens, labels_tens)
        loss_ones = criterion(out_ones, labels_ones)
        total_loss = loss_full + lambda_tens * loss_tens + lambda_ones * loss_ones

        total_loss.backward()
        optimizer.step()

        batch_size = images.size(0)
        running["num_samples"] += batch_size
        running["total_loss"] += total_loss.item() * batch_size
        running["loss_full"] += loss_full.item() * batch_size
        running["loss_tens"] += loss_tens.item() * batch_size
        running["loss_ones"] += loss_ones.item() * batch_size

        preds_full = out_full.argmax(dim=1)
        running["correct_full"] += (preds_full == labels_full).sum().item()

        n = running["num_samples"]
        progress.set_postfix(
            loss=f"{running['total_loss']/n:.4f}",
            acc=f"{running['correct_full']/n:.4f}",
        )

    n = running["num_samples"]
    return {
        "total_loss": running["total_loss"] / n,
        "loss_full": running["loss_full"] / n,
        "loss_tens": running["loss_tens"] / n,
        "loss_ones": running["loss_ones"] / n,
        "acc_full": running["correct_full"] / n,
    }


@torch.no_grad()
def validate(
    model: nn.Module,
    dataloader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
    epoch: int,
    num_epochs: int,
    lambda_tens: float = 1.0,
    lambda_ones: float = 1.0,
) -> Dict[str, float]:
    model.eval()
    running = {
        "total_loss": 0.0,
        "loss_full": 0.0,
        "loss_tens": 0.0,
        "loss_ones": 0.0,
        "correct_full": 0,
        "num_samples": 0,
    }

    progress = tqdm(dataloader, desc=f"Epoch {epoch}/{num_epochs} [val]")
    for images, labels_full, labels_tens, labels_ones in progress:
        images = images.to(device, non_blocking=True)
        labels_full = labels_full.to(device, dtype=torch.long, non_blocking=True)
        labels_tens = labels_tens.to(device, dtype=torch.long, non_blocking=True)
        labels_ones = labels_ones.to(device, dtype=torch.long, non_blocking=True)

        out_full, out_tens, out_ones = model(images)
        loss_full = criterion(out_full, labels_full)
        loss_tens = criterion(out_tens, labels_tens)
        loss_ones = criterion(out_ones, labels_ones)
        total_loss = loss_full + lambda_tens * loss_tens + lambda_ones * loss_ones

        batch_size = images.size(0)
        running["num_samples"] += batch_size
        running["total_loss"] += total_loss.item() * batch_size
        running["loss_full"] += loss_full.item() * batch_size
        running["loss_tens"] += loss_tens.item() * batch_size
        running["loss_ones"] += loss_ones.item() * batch_size

        preds_full = out_full.argmax(dim=1)
        running["correct_full"] += (preds_full == labels_full).sum().item()

        n = running["num_samples"]
        progress.set_postfix(
            loss=f"{running['total_loss']/n:.4f}",
            acc=f"{running['correct_full']/n:.4f}",
        )

    n = running["num_samples"]
    return {
        "total_loss": running["total_loss"] / n,
        "loss_full": running["loss_full"] / n,
        "loss_tens": running["loss_tens"] / n,
        "loss_ones": running["loss_ones"] / n,
        "acc_full": running["correct_full"] / n,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train multi-task jersey number classifier")

    # Data paths (SoccerNet JSON or CSV format)
    parser.add_argument("--train-annotations", type=str, required=True,
                        help="Path to train annotations (e.g., data/SoccerNet/train/train_gt.json)")
    parser.add_argument("--train-images", type=str, required=True,
                        help="Path to train image dir (e.g., data/SoccerNet/train/images)")
    parser.add_argument("--val-annotations", type=str, default=None,
                        help="Path to val annotations (optional, enables early stopping)")
    parser.add_argument("--val-images", type=str, default=None,
                        help="Path to val image dir")

    # Training hyperparameters
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--num-workers", type=int, default=4)

    # Loss weights (proposal: lambda1=tens, lambda2=ones)
    parser.add_argument("--lambda-tens", type=float, default=1.0,
                        help="Loss weight for tens digit head")
    parser.add_argument("--lambda-ones", type=float, default=1.0,
                        help="Loss weight for ones digit head")

    # Early stopping
    parser.add_argument("--patience", type=int, default=7,
                        help="Early stopping patience (epochs without improvement)")

    # Checkpoints
    parser.add_argument("--checkpoint-dir", type=str, default="checkpoints")
    parser.add_argument("--no-pretrained", action="store_true",
                        help="Train from scratch (no ImageNet weights)")

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    # ── Data ──
    train_dataset = JerseyNumberMultitaskDataset(
        annotations_file=args.train_annotations,
        img_dir=args.train_images,
        mode="train",
        arch="resnet34",
    )
    train_loader = DataLoader(
        train_dataset,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=args.num_workers,
        pin_memory=torch.cuda.is_available(),
    )

    val_loader = None
    if args.val_annotations and args.val_images:
        val_dataset = JerseyNumberMultitaskDataset(
            annotations_file=args.val_annotations,
            img_dir=args.val_images,
            mode="val",
            arch="resnet34",
        )
        val_loader = DataLoader(
            val_dataset,
            batch_size=args.batch_size,
            shuffle=False,
            num_workers=args.num_workers,
            pin_memory=torch.cuda.is_available(),
        )

    # ── Model ──
    model = MultiTaskSTRRecognizer(pretrained=not args.no_pretrained).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = AdamW(model.parameters(), lr=args.lr)
    scheduler = CosineAnnealingLR(optimizer, T_max=args.epochs)

    # ── Checkpointing ──
    checkpoint_dir = Path(args.checkpoint_dir)
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    best_val_acc = 0.0
    patience_counter = 0

    # ── Training loop ──
    for epoch in range(1, args.epochs + 1):
        train_metrics = train_one_epoch(
            model=model,
            dataloader=train_loader,
            criterion=criterion,
            optimizer=optimizer,
            device=device,
            epoch=epoch,
            num_epochs=args.epochs,
            lambda_tens=args.lambda_tens,
            lambda_ones=args.lambda_ones,
        )
        scheduler.step()

        print(
            f"[train] epoch={epoch} "
            f"loss={train_metrics['total_loss']:.4f} "
            f"(full={train_metrics['loss_full']:.4f} "
            f"tens={train_metrics['loss_tens']:.4f} "
            f"ones={train_metrics['loss_ones']:.4f}) "
            f"acc={train_metrics['acc_full']:.4f} "
            f"lr={scheduler.get_last_lr()[0]:.6f}"
        )

        # ── Validation ──
        if val_loader is not None:
            val_metrics = validate(
                model=model,
                dataloader=val_loader,
                criterion=criterion,
                device=device,
                epoch=epoch,
                num_epochs=args.epochs,
                lambda_tens=args.lambda_tens,
                lambda_ones=args.lambda_ones,
            )
            print(
                f"[val]   epoch={epoch} "
                f"loss={val_metrics['total_loss']:.4f} "
                f"acc={val_metrics['acc_full']:.4f}"
            )

            # ── Best model checkpoint ──
            if val_metrics["acc_full"] > best_val_acc:
                best_val_acc = val_metrics["acc_full"]
                patience_counter = 0
                best_path = checkpoint_dir / "best_multitask_resnet34.pth"
                torch.save(model.state_dict(), best_path)
                print(f"  ★ New best val acc: {best_val_acc:.4f} — saved {best_path}")
            else:
                patience_counter += 1
                print(f"  No improvement ({patience_counter}/{args.patience})")

            # ── Early stopping ──
            if patience_counter >= args.patience:
                print(f"\nEarly stopping at epoch {epoch} (no improvement for {args.patience} epochs)")
                print(f"Best val accuracy: {best_val_acc:.4f}")
                break

        # ── Regular checkpoint every 5 epochs ──
        if epoch % 5 == 0:
            ckpt_path = checkpoint_dir / f"multitask_resnet34_epoch_{epoch:03d}.pth"
            torch.save(model.state_dict(), ckpt_path)
            print(f"  Checkpoint: {ckpt_path}")

    # ── Final save ──
    final_path = checkpoint_dir / "multitask_resnet34_final.pth"
    torch.save(model.state_dict(), final_path)
    print(f"\nTraining complete. Final model: {final_path}")
    if val_loader is not None:
        print(f"Best validation accuracy: {best_val_acc:.4f}")


if __name__ == "__main__":
    main()
