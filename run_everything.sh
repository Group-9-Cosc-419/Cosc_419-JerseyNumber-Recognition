#!/bin/bash
# ============================================================
# run_everything.sh — COSC 419 Full Retrain on Crops
# Group 9 — Run this on vast.ai with GPU
#
# Does THREE things in one session:
#   1. Generates training crops (stages 1-6 on train split)
#   2. Retrains the multi-task model on crops
#   3. Runs inference on test crops
#
# PREREQUISITES:
#   - Repo cloned at /workspace/jersey-number-pipeline
#   - setup_env.sh already run
#   - SoccerNet data downloaded and unzipped
#   - Test crops already generated (from previous pipeline run)
#
# USAGE:
#   chmod +x run_everything.sh
#   ./run_everything.sh 2>&1 | tee training_log.txt
# ============================================================

set -e
cd /workspace/jersey-number-pipeline

echo "============================================"
echo "  PHASE 1: Generate Training Crops"
echo "============================================"

# ── 1a. Feature generation on train set ──
FEATURES_DIR="out/SoccerNetResults/train/features"
if [ -d "$FEATURES_DIR" ] && [ "$(ls -1 "$FEATURES_DIR" 2>/dev/null | wc -l)" -gt 100 ]; then
    echo "[1/6] Features already exist, skipping."
else
    echo "[1/6] Generating features (ReID) on train set..."
    PYTHONPATH="/workspace/jersey-number-pipeline/reid/centroids-reid:$PYTHONPATH" \
        python3 centroid_reid.py \
        --tracklets_folder data/SoccerNet/train/images \
        --output_folder out/SoccerNetResults/train/features
fi

# ── 1b. Gaussian outlier filtering ──
GAUSS_FILE="out/SoccerNetResults/train/main_subject_gauss_th=3.5_r=3.json"
if [ -f "$GAUSS_FILE" ]; then
    echo "[2/6] Gaussian filter results exist, skipping."
else
    echo "[2/6] Running Gaussian outlier filtering on train set..."
    python3 gaussian_outliers.py \
        --tracklets_folder data/SoccerNet/train/images \
        --output_folder out/SoccerNetResults/train/features
    # Copy to expected location
    cp out/SoccerNetResults/train/features/main_subject_gauss*.json out/SoccerNetResults/train/ 2>/dev/null || true
fi

# ── 1c. Legibility + Pose + Crops via main.py ──
echo "[3/6] Running legibility classifier on train set..."
python3 -c "
import sys, argparse
sys.path.insert(0, '/workspace/jersey-number-pipeline')
import main

args = argparse.Namespace()
args.dataset = 'SoccerNet'
args.part = 'train'
args.topk = 5
args.pipeline = {
    'soccer_ball_filter': True,
    'feat': False,
    'filter': False,
    'legible': True,
    'legible_eval': True,
    'pose': True,
    'crops': False,
    'str': False,
    'combine': False,
    'eval': False,
}
main.soccer_net_pipeline(args)
"

# ── 1d. Pose estimation (standalone, conda run fails) ──
POSE_RESULTS="out/SoccerNetResults/pose_results_train.json"
if [ -f "$POSE_RESULTS" ]; then
    echo "[4/6] Pose results exist, skipping."
else
    echo "[4/6] Running pose estimation on train set..."
    python3 pose.py \
        pose/ViTPose/configs/body/2d_kpt_sview_rgb_img/topdown_heatmap/coco/ViTPose_huge_coco_256x192.py \
        pose/ViTPose/checkpoints/vitpose-h.pth \
        --img-root / \
        --json-file out/SoccerNetResults/pose_input_train.json \
        --out-json out/SoccerNetResults/pose_results_train.json
fi

# ── 1e. Generate crops ──
echo "[5/6] Generating crops from train set..."
python3 -c "
import sys, argparse
sys.path.insert(0, '/workspace/jersey-number-pipeline')
import main

args = argparse.Namespace()
args.dataset = 'SoccerNet'
args.part = 'train'
args.topk = 5
args.pipeline = {
    'soccer_ball_filter': False,
    'feat': False,
    'filter': False,
    'legible': False,
    'legible_eval': False,
    'pose': False,
    'crops': True,
    'str': False,
    'combine': False,
    'eval': False,
}
main.soccer_net_pipeline(args)
"

# ── 1f. Organize crops by tracklet ──
echo "[6/6] Organizing crops into tracklet folders..."
python3 -c "
import os, shutil

# Organize flat crops into tracklet folders
for split in ['train', 'test']:
    src = f'out/SoccerNetResults/{split}/crops/imgs'
    dst = f'out/SoccerNetResults/{split}/crops_organized'

    if os.path.isdir(dst) and len(os.listdir(dst)) > 10:
        print(f'{split} crops already organized')
        continue

    if not os.path.isdir(src):
        # Try alternative path
        src = f'out/SoccerNetResults/crops/imgs'
        if not os.path.isdir(src):
            print(f'WARNING: no crops found for {split}')
            continue

    os.makedirs(dst, exist_ok=True)
    count = 0
    for fname in os.listdir(src):
        if not fname.endswith('.jpg'):
            continue
        tracklet = fname.split('_')[0]
        tracklet_dir = os.path.join(dst, tracklet)
        os.makedirs(tracklet_dir, exist_ok=True)
        shutil.copy2(os.path.join(src, fname), os.path.join(tracklet_dir, fname))
        count += 1
    print(f'{split}: organized {count} crops into {len(os.listdir(dst))} tracklets')
"

echo ""
echo "============================================"
echo "  PHASE 2: Retrain on Crops"
echo "============================================"

# First, create a ground truth JSON that maps tracklet IDs to jersey numbers
# using only tracklets that have crops
python3 -c "
import json, os

for split, gt_file in [('train', 'data/SoccerNet/train/train_gt.json'), ('test', 'data/SoccerNet/test/test_gt.json')]:
    crops_dir = f'out/SoccerNetResults/{split}/crops_organized'
    if not os.path.isdir(crops_dir):
        crops_dir = f'out/SoccerNetResults/crops_organized'

    with open(gt_file) as f:
        gt = json.load(f)

    # Filter to only tracklets that have crops
    filtered = {}
    for t in os.listdir(crops_dir):
        if t in gt:
            filtered[t] = gt[t]

    out_path = f'out/{split}_crops_gt.json'
    with open(out_path, 'w') as f:
        json.dump(filtered, f)
    print(f'{split}: {len(filtered)} tracklets with crops (out of {len(gt)} total)')
"

echo "Training multi-task model on crops..."
python3 train_multitask.py \
    --train-annotations out/train_crops_gt.json \
    --train-images out/SoccerNetResults/train/crops_organized \
    --val-annotations out/test_crops_gt.json \
    --val-images out/SoccerNetResults/test/crops_organized \
    --epochs 50 \
    --batch-size 64 \
    --lr 1e-4 \
    --num-workers 4 \
    --checkpoint-dir checkpoints_crops

echo ""
echo "============================================"
echo "  PHASE 3: Inference on Test Crops"
echo "============================================"

echo "Running inference..."
python3 inference_multitask.py \
    --checkpoint checkpoints_crops/best_multitask_resnet34.pth \
    --data_root out/SoccerNetResults/test/crops_organized \
    --result_file out/SoccerNetResults/jersey_id_results.json \
    --theta 0.5 \
    --batch_size 64

echo ""
echo "============================================"
echo "  PHASE 4: Evaluate"
echo "============================================"

python3 -c "
import sys, argparse
sys.path.insert(0, '/workspace/jersey-number-pipeline')
import helpers, main

args = argparse.Namespace()
args.dataset = 'SoccerNet'
args.part = 'test'
args.topk = 0
args.pipeline = {
    'soccer_ball_filter': False, 'feat': False, 'filter': False,
    'legible': False, 'legible_eval': False, 'pose': False,
    'crops': False, 'str': False,
    'combine': True, 'eval': True,
}
main.soccer_net_pipeline(args)
"

echo ""
echo "============================================"
echo "  DONE!"
echo "  Download checkpoints_crops/ and results"
echo "  Then DESTROY the instance"
echo "============================================"
