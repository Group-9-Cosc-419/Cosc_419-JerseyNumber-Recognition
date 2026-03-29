from __future__ import annotations

import torch
from torch import nn


def _build_svtr_encoder(freeze: bool = False):
    """Load SVTR encoder pretrained on scene text recognition."""
    import timm
    encoder = timm.create_model('svtr_tiny', pretrained=True, num_classes=0)
    feature_dim = encoder.num_features
    if freeze:
        for param in encoder.parameters():
            param.requires_grad = False
    return encoder, feature_dim


class MultiTaskSTRRecognizer(nn.Module):
    """
    Shared-backbone multi-task STR model for jersey number recognition.

    Backbone changed from ResNet-34 (ImageNet, image classification)
    to SVTR (scene text recognition, pretrained on text data).

    Outputs:
    - full head: 100 classes (0-99)
    - tens head: 11 classes (0-9 + blank at index 10)
    - ones head: 10 classes (0-9)
    """

    def __init__(self, pretrained: bool = True, freeze_backbone: bool = False) -> None:
        super().__init__()

        self.backbone, feature_dim = _build_svtr_encoder(freeze=freeze_backbone)

        self.head_full = nn.Linear(feature_dim, 100)
        self.head_tens = nn.Linear(feature_dim, 11)
        self.head_ones = nn.Linear(feature_dim, 10)

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        features = self.backbone(x)
        out_full = self.head_full(features)
        out_tens = self.head_tens(features)
        out_ones = self.head_ones(features)
        return out_full, out_tens, out_ones