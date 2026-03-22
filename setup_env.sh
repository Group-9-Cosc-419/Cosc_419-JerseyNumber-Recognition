#!/bin/bash
# ============================================================
# setup_env.sh — COSC 419 Jersey Number Pipeline Environment
# Group 9 — Run this ONCE when you spin up a new instance
#
# USAGE:
#   chmod +x setup_env.sh
#   ./setup_env.sh
#
# ASSUMES: Ubuntu/Debian with NVIDIA GPU + CUDA drivers already present
#          (Colab, vast.ai, Lambda, etc. all satisfy this)
# ============================================================

set -e  # Stop on first error

echo "============================================"
echo "  COSC 419 — Environment Setup"
echo "============================================"

# ── 0. Detect CUDA version ──
echo ""
echo "[0/6] Detecting CUDA version..."
if command -v nvcc &> /dev/null; then
    CUDA_VER=$(nvcc --version | grep "release" | sed 's/.*release //' | sed 's/,.*//')
    echo "  Found CUDA $CUDA_VER"
else
    CUDA_VER=$(nvidia-smi | grep "CUDA Version" | awk '{print $9}')
    echo "  Found CUDA $CUDA_VER (from nvidia-smi)"
fi

# ── 1. Install PyTorch (must match CUDA) ──
echo ""
echo "[1/6] Installing PyTorch..."
# Default: CUDA 12.1 (vast.ai default). Change if needed.
pip install torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cu121 --quiet

# Verify
python -c "import torch; print(f'  PyTorch {torch.__version__} | CUDA available: {torch.cuda.is_available()} | Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"CPU\"}')"

# ── 2. Core dependencies ──
echo ""
echo "[2/6] Installing core dependencies..."
pip install \
    numpy==1.23.5 \
    scipy==1.11.4 \
    pandas \
    opencv-python==4.8.1.78 \
    pillow \
    scikit-learn \
    matplotlib \
    tqdm \
    pyyaml \
    einops \
    lmdb \
    shapely \
    gdown \
    SoccerNet \
    --quiet

# ── 3. ReID dependencies ──
echo ""
echo "[3/6] Installing ReID dependencies..."
pip install \
    pytorch-lightning==1.9.5 \
    torchmetrics==0.11.4 \
    yacs \
    --quiet

# ── 4. Pose dependencies (timm 0.4.9 first) ──
echo ""
echo "[4/6] Installing pose dependencies..."
pip install timm==0.4.9 --quiet
pip install \
    mmcv==1.5.0 \
    mmdet \
    xtcocotools \
    chumpy \
    json_tricks \
    munkres \
    --quiet

# ── 5. Install ViTPose (no-deps to avoid conflicts) ──
echo ""
echo "[5/6] Installing ViTPose..."
if [ -d "pose/ViTPose" ]; then
    pip install -e pose/ViTPose/ --no-deps --quiet
    echo "  ViTPose installed"
else
    echo "  WARNING: pose/ViTPose not found. Clone the repo first."
fi

# ── 6. Verify ──
echo ""
echo "[6/6] Verifying installation..."
python -c "
import torch, numpy, scipy, cv2
import torchmetrics
import pytorch_lightning as pl
print(f'  torch={torch.__version__}')
print(f'  numpy={numpy.__version__}')
print(f'  scipy={scipy.__version__}')
print(f'  opencv={cv2.__version__}')
print(f'  pytorch-lightning={pl.__version__}')
print(f'  torchmetrics={torchmetrics.__version__}')
print(f'  CUDA={torch.cuda.is_available()}')
"

echo ""
echo "============================================"
echo "  Setup complete!"
echo ""
echo "  IMPORTANT: Before running STR (PARSeq),"
echo "  you MUST switch timm versions:"
echo "    pip install timm==0.6.13 nltk"
echo ""
echo "  This will break pose if you re-run it."
echo "  Run pose FIRST, then switch timm for STR."
echo "============================================"
