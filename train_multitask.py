from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Tuple

import torch
from torch import nn
from torch.optim import Adam
from torch.utils.data import DataLoader, Dataset
from torchvision import datasets, transforms
from tqdm import tqdm

from recognition import MultiTaskSTRRecognizer


class MultiTaskImageFolderDataset(Dataset):
    """
    Wrap torchvision ImageFolder and emit:
    (image, label_full, label_tens, label_ones)
    """

    def __init__(self, root: str, image_transform: transforms.Compose) -> None:
        self.base_dataset = datasets.ImageFolder(root=root, transform=image_transform)
        self.idx_to_full_label = self._build_label_map(self.base_dataset.class_to_idx)

    @staticmethod
    def _build_label_map(class_to_idx: Dict[str, int]) -> Dict[int, int]:
        idx_to_full_label: Dict[int, int] = {}
        for class_name, class_idx in class_to_idx.items():
            try:
                full_label = int(class_name)
            except ValueError as exc:
                raise ValueError(
                    f"Class folder '{class_name}' is not numeric. Expected folder names 0..99."
                ) from exc

            if not (0 <= full_label <= 99):
                raise ValueError(
                    f"Invalid class folder '{class_name}'. Expected jersey labels in [0, 99]."
                )
            idx_to_full_label[class_idx] = full_label
        return idx_to_full_label

    @staticmethod
    def split_digits(full_label: int) -> Tuple[int, int]:
        if full_label < 10:
            return 10, full_label
        return full_label // 10, full_label % 10

    def __len__(self) -> int:
        return len(self.base_dataset)

    def __getitem__(self, index: int):
        image, class_idx = self.base_dataset[index]
        label_full = self.idx_to_full_label[class_idx]
        label_tens, label_ones = self.split_digits(label_full)
        return image, label_full, label_tens, label_ones


def train_one_epoch(
    model: nn.Module,
    dataloader: DataLoader,
    criterion: nn.Module,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
    epoch: int,
    num_epochs: int,
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
        total_loss = loss_full + loss_tens + loss_ones

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

        avg_total = running["total_loss"] / running["num_samples"]
        avg_full = running["loss_full"] / running["num_samples"]
        avg_tens = running["loss_tens"] / running["num_samples"]
        avg_ones = running["loss_ones"] / running["num_samples"]
        avg_acc = running["correct_full"] / running["num_samples"]
        progress.set_postfix(
            total=f"{avg_total:.4f}",
            full=f"{avg_full:.4f}",
            tens=f"{avg_tens:.4f}",
            ones=f"{avg_ones:.4f}",
            acc_full=f"{avg_acc:.4f}",
        )

    num_samples = running["num_samples"]
    return {
        "total_loss": running["total_loss"] / num_samples,
        "loss_full": running["loss_full"] / num_samples,
        "loss_tens": running["loss_tens"] / num_samples,
        "loss_ones": running["loss_ones"] / num_samples,
        "acc_full": running["correct_full"] / num_samples,
    }


@torch.no_grad()
def validate_one_epoch(
    model: nn.Module,
    dataloader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
    epoch: int,
    num_epochs: int,
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
        total_loss = loss_full + loss_tens + loss_ones

        batch_size = images.size(0)
        running["num_samples"] += batch_size
        running["total_loss"] += total_loss.item() * batch_size
        running["loss_full"] += loss_full.item() * batch_size
        running["loss_tens"] += loss_tens.item() * batch_size
        running["loss_ones"] += loss_ones.item() * batch_size

        preds_full = out_full.argmax(dim=1)
        running["correct_full"] += (preds_full == labels_full).sum().item()

        avg_total = running["total_loss"] / running["num_samples"]
        avg_full = running["loss_full"] / running["num_samples"]
        avg_tens = running["loss_tens"] / running["num_samples"]
        avg_ones = running["loss_ones"] / running["num_samples"]
        avg_acc = running["correct_full"] / running["num_samples"]
        progress.set_postfix(
            total=f"{avg_total:.4f}",
            full=f"{avg_full:.4f}",
            tens=f"{avg_tens:.4f}",
            ones=f"{avg_ones:.4f}",
            acc_full=f"{avg_acc:.4f}",
        )

    num_samples = running["num_samples"]
    return {
        "total_loss": running["total_loss"] / num_samples,
        "loss_full": running["loss_full"] / num_samples,
        "loss_tens": running["loss_tens"] / num_samples,
        "loss_ones": running["loss_ones"] / num_samples,
        "acc_full": running["correct_full"] / num_samples,
    }


def build_dataloader(
    data_root: str, batch_size: int, num_workers: int, shuffle: bool
) -> DataLoader:
    image_transform = transforms.Compose(
        [
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
            ),
        ]
    )
    dataset = MultiTaskImageFolderDataset(root=data_root, image_transform=image_transform)
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        pin_memory=torch.cuda.is_available(),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--train-root", type=str, required=True)
    parser.add_argument("--val-root", type=str, default=None)
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--num-workers", type=int, default=4)
    parser.add_argument("--checkpoint-dir", type=str, default="checkpoints")
    parser.add_argument("--no-pretrained", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    train_loader = build_dataloader(
        data_root=args.train_root,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        shuffle=True,
    )

    val_loader = None
    if args.val_root:
        val_loader = build_dataloader(
            data_root=args.val_root,
            batch_size=args.batch_size,
            num_workers=args.num_workers,
            shuffle=False,
        )

    model = MultiTaskSTRRecognizer(pretrained=not args.no_pretrained).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = Adam(model.parameters(), lr=1e-4)

    checkpoint_dir = Path(args.checkpoint_dir)
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    for epoch in range(1, args.epochs + 1):
        train_metrics = train_one_epoch(
            model=model,
            dataloader=train_loader,
            criterion=criterion,
            optimizer=optimizer,
            device=device,
            epoch=epoch,
            num_epochs=args.epochs,
        )

        print(
            f"[train] epoch={epoch} "
            f"total={train_metrics['total_loss']:.4f} "
            f"full={train_metrics['loss_full']:.4f} "
            f"tens={train_metrics['loss_tens']:.4f} "
            f"ones={train_metrics['loss_ones']:.4f} "
            f"acc_full={train_metrics['acc_full']:.4f}"
        )

        if val_loader is not None:
            val_metrics = validate_one_epoch(
                model=model,
                dataloader=val_loader,
                criterion=criterion,
                device=device,
                epoch=epoch,
                num_epochs=args.epochs,
            )
            print(
                f"[val]   epoch={epoch} "
                f"total={val_metrics['total_loss']:.4f} "
                f"full={val_metrics['loss_full']:.4f} "
                f"tens={val_metrics['loss_tens']:.4f} "
                f"ones={val_metrics['loss_ones']:.4f} "
                f"acc_full={val_metrics['acc_full']:.4f}"
            )

        if epoch % 5 == 0:
            ckpt_path = checkpoint_dir / f"multitask_resnet34_epoch_{epoch:03d}.pth"
            torch.save(model.state_dict(), ckpt_path)
            print(f"Saved checkpoint: {ckpt_path}")


if __name__ == "__main__":
    main()

