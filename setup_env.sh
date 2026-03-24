#!/bin/bash
# ============================================================
# setup_env.sh — COSC 419 Jersey Number Pipeline Environment
# Group 9 — Run this ONCE when you spin up a new instance
#
# Handles: Colab, vast.ai, Lambda, any Linux + GPU
# Fixes: setuptools, numpy binary compat, mmcv on Python 3.12,
#        torch.load weights_only, HuggingFace datasets conflict
# ============================================================

set -e

echo "============================================"
echo "  COSC 419 — Environment Setup"
echo "============================================"

# ── 0. Prerequisites ──
echo ""
echo "[0/7] Installing prerequisites..."
pip install setuptools wheel --quiet

# ── 1. Detect environment ──
echo ""
echo "[1/7] Detecting environment..."
TORCH_EXISTS=$(python -c "import torch; print('yes')" 2>/dev/null || echo "no")

if [ "$TORCH_EXISTS" = "yes" ]; then
    echo "  PyTorch already installed — keeping existing version"
    python -c "import torch; print(f'  torch={torch.__version__} | CUDA={torch.cuda.is_available()}')"
fi

# ── 2. Install PyTorch (only if not present) ──
echo ""
echo "[2/7] PyTorch..."
if [ "$TORCH_EXISTS" = "yes" ]; then
    echo "  Skipped (already installed)"
else
    echo "  Installing fresh..."
    if python -c "import subprocess; r=subprocess.run(['nvidia-smi'],capture_output=True); exit(0 if r.returncode==0 else 1)" 2>/dev/null; then
        pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121 --quiet
    else
        pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu --quiet
    fi
    python -c "import torch; print(f'  torch={torch.__version__} | CUDA={torch.cuda.is_available()}')"
fi

# ── 3. Core dependencies ──
echo ""
echo "[3/7] Installing core dependencies..."
pip install \
    numpy==1.26.4 \
    scipy \
    pandas \
    opencv-python \
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

# ── 4. ReID dependencies ──
echo ""
echo "[4/7] Installing ReID dependencies..."
pip install \
    pytorch-lightning==1.9.5 \
    torchmetrics==0.11.4 \
    yacs \
    --quiet

# ── 5. Pose dependencies ──
echo ""
echo "[5/7] Installing pose dependencies..."
pip install timm==0.4.9 --quiet

# mmcv 1.5.0 doesn't build on Python 3.12 — try it, fall back to 2.x
PYTHON_VER=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "  Python version: $PYTHON_VER"
if pip install mmcv==1.5.0 --quiet 2>/dev/null; then
    echo "  mmcv 1.5.0 installed"
else
    echo "  mmcv 1.5.0 failed (Python $PYTHON_VER), trying mmcv 2.x..."
    pip install "mmcv>=2.0.0" --quiet 2>/dev/null || echo "  WARNING: mmcv install failed — pose may not work"
fi
pip install mmdet xtcocotools chumpy json_tricks munkres --quiet 2>/dev/null || true

# ── 6. Install ViTPose ──
echo ""
echo "[6/7] Installing ViTPose..."
if [ -d "pose/ViTPose" ]; then
    pip install -e pose/ViTPose/ --no-deps --quiet
    echo "  ViTPose installed"
else
    echo "  WARNING: pose/ViTPose not found. Clone the repo first."
fi

# ── 7. Patches & Verify ──
echo ""
echo "[7/7] Applying patches and verifying..."

# Patch torch.load for PyTorch 2.6+ (old checkpoints need weights_only=False)
python -c "
import os, glob

# Find and patch lightning files
for pkg in ['lightning_fabric', 'pytorch_lightning']:
    try:
        mod = __import__(pkg)
        pkg_dir = os.path.dirname(mod.__file__)
        for pyfile in glob.glob(os.path.join(pkg_dir, '**', '*.py'), recursive=True):
            try:
                with open(pyfile, 'r') as f:
                    content = f.read()
                if 'torch.load(f, map_location=map_location)' in content and 'weights_only' not in content:
                    content = content.replace(
                        'torch.load(f, map_location=map_location)',
                        'torch.load(f, map_location=map_location, weights_only=False)'
                    )
                    with open(pyfile, 'w') as f:
                        f.write(content)
            except:
                pass
    except ImportError:
        pass
print('  torch.load patched')
"

# Uninstall HuggingFace datasets (conflicts with centroids-reid local datasets module)
pip uninstall datasets -y --quiet 2>/dev/null || true
echo "  HuggingFace datasets removed"

# Verify
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
echo "============================================"
