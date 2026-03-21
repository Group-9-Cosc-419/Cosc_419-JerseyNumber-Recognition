from __future__ import annotations

import torch
from torch import nn
from torchvision import models


def _build_resnet34(pretrained: bool = True) -> nn.Module:
    """Build a ResNet34 while remaining compatible across torchvision versions."""
    try:
        weights = models.ResNet34_Weights.DEFAULT if pretrained else None
        return models.resnet34(weights=weights)
    except (AttributeError, TypeError):
        return models.resnet34(pretrained=pretrained)


class MultiTaskSTRRecognizer(nn.Module):
    """
    Shared-backbone multi-task STR model for jersey number recognition.

    Outputs:
    - full head: 100 classes (0-99)
    - tens head: 11 classes (0-9 + blank at index 10)
    - ones head: 10 classes (0-9)
    """

    def __init__(self, pretrained: bool = True, freeze_backbone: bool = False) -> None:
        super().__init__()

        backbone = _build_resnet34(pretrained=pretrained)
        feature_dim = backbone.fc.in_features
        backbone.fc = nn.Identity()
        self.backbone = backbone

        if freeze_backbone:
            for param in self.backbone.parameters():
                param.requires_grad = False

        self.head_full = nn.Linear(feature_dim, 100)
        self.head_tens = nn.Linear(feature_dim, 11)
        self.head_ones = nn.Linear(feature_dim, 10)

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        features = self.backbone(x)
        out_full = self.head_full(features)
        out_tens = self.head_tens(features)
        out_ones = self.head_ones(features)
        return out_full, out_tens, out_ones

