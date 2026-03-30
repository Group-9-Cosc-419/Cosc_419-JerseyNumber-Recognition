# Copyright (c) OpenMMLab. All rights reserved.
import os
import warnings
import json
import sys

ROOT = './pose/ViTPose/'
sys.path.append(str(ROOT))  # add ROOT to PATH

from argparse import ArgumentParser

from xtcocotools.coco import COCO
from tqdm import tqdm

from mmpose.apis import (inference_top_down_pose_model, init_pose_model,
                         vis_pose_result)
from mmpose.datasets import DatasetInfo


def main():
    """Visualize the demo images.

    Require the json_file containing boxes.
    """
    parser = ArgumentParser()
    parser.add_argument('pose_config', help='Config file for detection')
    parser.add_argument('pose_checkpoint', help='Checkpoint file')
    parser.add_argument('--img-root', type=str, default='', help='Image root')
    parser.add_argument(
        '--json-file',
        type=str,
        default='',
        help='Json file containing image info.')
    parser.add_argument(
        '--out-json',
        type=str,
        default='',
        help='Json file containing results.')
    parser.add_argument(
        '--show',
        action='store_true',
        default=False,
        help='whether to show img')
    parser.add_argument(
        '--out-img-root',
        type=str,
        default='',
        help='Root of the output img file. '
             'Default not saving the visualization images.')
    parser.add_argument(
        '--device', default='cuda:0', help='Device used for inference')
    parser.add_argument(
        '--kpt-thr', type=float, default=0.3, help='Keypoint score threshold')
    parser.add_argument(
        '--radius',
        type=int,
        default=4,
        help='Keypoint radius for visualization')
    parser.add_argument(
        '--thickness',
        type=int,
        default=1,
        help='Link thickness for visualization')
    parser.add_argument(
        '--batch-size',
        type=int,
        default=32,
        help='Batch size for pose inference per image')
    parser.add_argument(
        '--save-every',
        type=int,
        default=500,
        help='Save intermediate results every N images')
    parser.add_argument(
        '--resume',
        action='store_true',
        default=False,
        help='Resume from existing partial output json')

    args = parser.parse_args()

    print(f"[pose.py] batch_size={args.batch_size}, save_every={args.save_every}, resume={args.resume}")
    print(f"[pose.py] show={args.show}, out_img_root={args.out_img_root}")

    coco = COCO(args.json_file)
    # build the pose model from a config file and a checkpoint file
    pose_model = init_pose_model(
        args.pose_config, args.pose_checkpoint, device=args.device.lower())

    dataset = pose_model.cfg.data['test']['type']
    dataset_info = pose_model.cfg.data['test'].get('dataset_info', None)
    if dataset_info is None:
        warnings.warn(
            'Please set `dataset_info` in the config.'
            'Check https://github.com/open-mmlab/mmpose/pull/663 for details.',
            DeprecationWarning)
    else:
        dataset_info = DatasetInfo(dataset_info)

    img_keys = list(coco.imgs.keys())
    total_images = len(img_keys)
    print(f"[pose.py] Total images to process: {total_images}")

    # optional
    return_heatmap = False
    output_layer_names = None

    # --- Resume support ---
    results = []
    processed_ids = set()
    start_idx = 0

    if args.resume and args.out_json and os.path.exists(args.out_json):
        try:
            with open(args.out_json, 'r') as fp:
                existing = json.load(fp)
            results = existing.get("pose_results", [])
            processed_ids = {r["id"] for r in results}
            print(f"[pose.py] Resuming: found {len(results)} already processed results")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[pose.py] Could not resume from {args.out_json}: {e}. Starting fresh.")
            results = []
            processed_ids = set()

    # --- Main loop with progress bar ---
    saved_count = len(results)

    for i in tqdm(range(total_images), desc="Pose estimation", unit="img",
                  dynamic_ncols=True, miniters=1):
        image_id = img_keys[i]

        # Skip already processed (resume mode)
        if image_id in processed_ids:
            continue

        image = coco.loadImgs(image_id)[0]
        image_name = os.path.join(args.img_root, image['file_name'])
        ann_ids = coco.getAnnIds(image_id)

        # make person bounding boxes
        person_results = []
        for ann_id in ann_ids:
            person = {}
            ann = coco.anns[ann_id]
            person['bbox'] = ann['bbox']
            person_results.append(person)

        if len(person_results) == 0:
            continue

        # --- Batch the bounding boxes for this image ---
        all_pose_results = []
        for batch_start in range(0, len(person_results), args.batch_size):
            batch = person_results[batch_start:batch_start + args.batch_size]

            pose_results, _ = inference_top_down_pose_model(
                pose_model,
                image_name,
                batch,
                bbox_thr=None,
                format='xywh',
                dataset=dataset,
                dataset_info=dataset_info,
                return_heatmap=return_heatmap,
                outputs=output_layer_names)
            all_pose_results.extend(pose_results)

        if len(all_pose_results) > 0:
            results.append({
                "img_name": image['file_name'],
                "id": image_id,
                "keypoints": all_pose_results[0]['keypoints'].tolist()
            })

        # Visualization (only if requested)
        if args.out_img_root != '':
            os.makedirs(args.out_img_root, exist_ok=True)
            out_file = os.path.join(args.out_img_root, f'vis_{i}.jpg')
            vis_pose_result(
                pose_model,
                image_name,
                all_pose_results,
                dataset=dataset,
                dataset_info=dataset_info,
                kpt_score_thr=args.kpt_thr,
                radius=args.radius,
                thickness=args.thickness,
                show=args.show,
                out_file=out_file)

        # --- Incremental save ---
        if args.out_json and (len(results) - saved_count) >= args.save_every:
            with open(args.out_json, 'w') as fp:
                json.dump({"pose_results": results}, fp)
            saved_count = len(results)
            tqdm.write(f"[checkpoint] Saved {len(results)} results to {args.out_json}")

    # Final save
    if args.out_json:
        with open(args.out_json, 'w') as fp:
            json.dump({"pose_results": results}, fp)
        print(f"[pose.py] Done! Saved {len(results)} results to {args.out_json}")


if __name__ == '__main__':
    main()
