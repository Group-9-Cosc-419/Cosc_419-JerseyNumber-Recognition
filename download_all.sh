#!/bin/bash
# ============================================================
# download_all.sh — COSC 419 Jersey Number Pipeline
# Group 9 — Downloads EVERYTHING: repos, models, weights, data
#
# USAGE:
#   chmod +x download_all.sh
#   ./download_all.sh
#
# Run this AFTER setup_env.sh. Safe to re-run (skips existing files).
# Does NOT need a GPU — run on free Colab or cheap CPU instance.
# ============================================================

set -e

REPO_DIR="${REPO_DIR:-$(pwd)}"
cd "$REPO_DIR"

echo "============================================"
echo "  COSC 419 — Download All Assets"
echo "  Working dir: $REPO_DIR"
echo "============================================"

# ── 1. Clone sub-repos ──
echo ""
echo "[1/4] Cloning sub-repositories..."

declare -A REPOS=(
    ["pose/ViTPose"]="https://github.com/ViTAE-Transformer/ViTPose.git"
    ["reid/centroids-reid"]="https://github.com/mikwieczorek/centroids-reid.git"
    ["str/parseq"]="https://github.com/baudm/parseq.git"
    ["sam"]="https://github.com/davda54/sam"
)

for dest in "${!REPOS[@]}"; do
    if [ -d "$dest" ]; then
        echo "  $dest — already exists, skipping"
    else
        echo "  $dest — cloning..."
        git clone --recurse-submodules "${REPOS[$dest]}" "$dest"
    fi
done

# ── 2. Create model directories ──
echo ""
echo "[2/4] Creating model directories..."
mkdir -p models
mkdir -p reid/centroids-reid/models
mkdir -p pose/ViTPose/checkpoints

# ── 3. Download model weights ──
echo ""
echo "[3/4] Downloading model weights..."

python3 << 'PYEOF'
import os
import sys
import glob
import shutil

# Add repo to path so we can import configuration
sys.path.insert(0, os.getcwd())
import configuration as cfg

try:
    import gdown
except ImportError:
    os.system("pip install gdown --quiet")
    import gdown

# ── Pipeline models (pose, STR, legibility) ──
downloads = [
    (cfg.dataset["SoccerNet"]["pose_model_url"],       "pose/ViTPose/checkpoints/vitpose-h.pth"),
    (cfg.dataset["SoccerNet"]["str_model_url"],         cfg.dataset["SoccerNet"]["str_model"]),
    (cfg.dataset["SoccerNet"]["legibility_model_url"],  cfg.dataset["SoccerNet"]["legibility_model"]),
]

for url, path in downloads:
    if os.path.isfile(path):
        print(f"  {path} — already exists")
    else:
        print(f"  {path} — downloading...")
        gdown.download(url, path, quiet=False)

# ── ReID weights ──
reid_ckpt = "reid/centroids-reid/models/market1501_resnet50_256_128_epoch_120.ckpt"

if os.path.isfile(reid_ckpt):
    print(f"  ReID weights — already exist")
else:
    print(f"  ReID weights — downloading folder...")
    gdown.download_folder(
        "https://drive.google.com/drive/folders/1NWD2Q0JGasGm9HTcOy4ZqsIqK4-IfknK",
        output="reid/centroids-reid/models/",
        quiet=False
    )
    # Flatten any nested subfolder
    for ckpt in glob.glob("reid/centroids-reid/models/**/*.ckpt", recursive=True):
        dest = os.path.join("reid/centroids-reid/models", os.path.basename(ckpt))
        if ckpt != dest:
            shutil.copy2(ckpt, dest)
    print("  ReID weights downloaded")

print()
print("  Model summary:")
for d in ["models/", "reid/centroids-reid/models/", "pose/ViTPose/checkpoints/"]:
    if os.path.isdir(d):
        files = os.listdir(d)
        total_mb = sum(os.path.getsize(os.path.join(d, f)) / 1e6 for f in files if os.path.isfile(os.path.join(d, f)))
        print(f"    {d}: {len(files)} files, {total_mb:.0f} MB")
PYEOF

# ── 4. Download & prepare SoccerNet data ──
echo ""
echo "[4/4] Downloading SoccerNet data..."

DATA_IMAGES="data/SoccerNet/test/images"

if [ -d "$DATA_IMAGES" ] && [ "$(ls -1 "$DATA_IMAGES" 2>/dev/null | wc -l)" -gt 100 ]; then
    echo "  Data already present: $(ls -1 "$DATA_IMAGES" | wc -l) tracklets"
else
    echo "  Downloading SoccerNet jersey-2023 dataset..."
    python3 -c "
from SoccerNet.Downloader import SoccerNetDownloader as SNdl
dl = SNdl(LocalDirectory='data/SoccerNet')
dl.downloadDataTask(task='jersey-2023', split=['train','test','challenge'])
print('Download complete')
"

    echo "  Unzipping test set..."
    unzip -qo data/SoccerNet/jersey-2023/test.zip -d data/SoccerNet/jersey-2023/ 2>/dev/null || true

    echo "  Flattening directory structure..."
    python3 << 'PYEOF2'
import os, shutil

src = "data/SoccerNet/jersey-2023"
dst = "data/SoccerNet"

if os.path.isdir(src):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
    shutil.rmtree(src)
PYEOF2

    # Clean macOS artifacts
    find data/SoccerNet -name ".DS_Store" -delete 2>/dev/null || true

    echo "  Data ready: $(ls -1 "$DATA_IMAGES" 2>/dev/null | wc -l) tracklets"
fi

echo ""
echo "============================================"
echo "  All downloads complete!"
echo ""
echo "  To verify:"
echo "    ls models/"
echo "    ls reid/centroids-reid/models/"
echo "    ls pose/ViTPose/checkpoints/"
echo "    ls data/SoccerNet/test/images/ | head"
echo "============================================"
