from torch.utils.data import Dataset
import numpy as np
import torch
import os
import pandas as pd
import json
from PIL import Image
from torchvision import transforms

data_transforms = {
    'train': {
        'resnet':
            transforms.Compose([
            transforms.RandomGrayscale(),
            transforms.ColorJitter(brightness=.5, hue=.3),
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ]),
        'vit':
            transforms.Compose([
                transforms.RandomGrayscale(),
                transforms.ColorJitter(brightness=.5, hue=.3),
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ]),
        },

    'val': {
        'resnet':
            transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ]),
        'vit':
            transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    },
    'test': {
        'resnet':
        transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ]),
        'vit':
        transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ]),
    }
}


class JerseyNumberDataset(Dataset):
    def __init__(self, annotations_file, img_dir, mode='train', arch='resnet34'):
        if 'resnet' in arch:
            arch = 'resnet'
        self.transform = data_transforms[mode][arch]
        self.img_labels = pd.read_csv(annotations_file)
        unqiue_ids = np.unique(self.img_labels.iloc[:, 1].to_numpy())
        print(f"Datafile:{annotations_file}, number of labels:{len(self.img_labels)}, unique ids: {len(unqiue_ids)}")
        self.img_dir = img_dir

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.img_labels.iloc[idx, 0])
        image = Image.open(img_path).convert('RGB')
        label = self.img_labels.iloc[idx, 1]
        if self.transform:
            image = self.transform(image)
        return image, label


class JerseyNumberMultitaskDataset(Dataset):
    """
    Multi-task dataset for jersey number recognition.

    Loads from SoccerNet JSON format:
        {"tracklet_id": jersey_number, ...}
        e.g. {"0": 10, "1": 30, "2": 27, ...}

    Expands tracklets into individual frame samples:
        tracklet "0" with 578 frames -> 578 samples, all labeled jersey=10

    Each sample returns:
        (image, full_label, tens_label, ones_label)

    Label splitting:
        Single-digit (1-9):  tens=10 (NULL), ones=digit
        Two-digit (10-99):   tens=digit//10, ones=digit%10

    Filters out tracklets with label -1 (illegible).
    """

    TENS_NULL = 10  # Sentinel for single-digit jerseys in tens head

    def __init__(self, annotations_file, img_dir, mode='train', arch='resnet34'):
        if 'resnet' in arch:
            arch = 'resnet'
        self.transform = data_transforms[mode][arch]
        self.img_dir = img_dir

        # Load JSON: {"tracklet_id": jersey_number, ...}
        with open(annotations_file, 'r') as f:
            tracklet_labels = json.load(f)

        # Expand tracklets into individual frame samples
        # Each entry: (relative_image_path, jersey_number)
        self.samples = []
        skipped_tracklets = 0
        for tracklet_id, jersey_number in tracklet_labels.items():
            jersey_number = int(jersey_number)

            # Skip illegible tracklets (label = -1)
            if jersey_number < 0:
                skipped_tracklets += 1
                continue

            # Skip out-of-range labels
            if jersey_number > 99:
                skipped_tracklets += 1
                continue

            tracklet_dir = os.path.join(img_dir, tracklet_id)
            if not os.path.isdir(tracklet_dir):
                continue

            for frame_name in os.listdir(tracklet_dir):
                if frame_name.startswith('.'):  # skip .DS_Store etc.
                    continue
                frame_path = os.path.join(tracklet_id, frame_name)
                self.samples.append((frame_path, jersey_number))

        unique_labels = set(label for _, label in self.samples)
        print(f"Datafile: {annotations_file}")
        print(f"  Tracklets: {len(tracklet_labels)} total, {skipped_tracklets} skipped (illegible/invalid)")
        print(f"  Frames: {len(self.samples)}, unique jersey numbers: {len(unique_labels)}")

    def __len__(self):
        return len(self.samples)

    def get_digit_labels(self, label):
        """Split full jersey number into (tens_label, ones_label)."""
        label = int(label)
        if label < 10:
            return self.TENS_NULL, label
        return label // 10, label % 10

    def __getitem__(self, idx):
        frame_path, label_full = self.samples[idx]
        img_path = os.path.join(self.img_dir, frame_path)
        image = Image.open(img_path).convert('RGB')
        label_tens, label_ones = self.get_digit_labels(label_full)

        if self.transform:
            image = self.transform(image)

        return image, label_full, label_tens, label_ones


class UnlabelledJerseyNumberLegibilityDataset(Dataset):
    def __init__(self, image_paths, mode='test', arch='resnet18'):
        if 'resnet' in arch:
            arch = 'resnet'
        self.transform = data_transforms[mode][arch]
        self.image_paths = image_paths

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        image = Image.open(img_path).convert('RGB')
        if self.transform:
            image = self.transform(image)

        return image


class TrackletLegibilityDataset(Dataset):
    def __init__(self, annotations_file, parent_dir, mode='test', arch='resnet18'):
        if 'resnet' in arch:
            arch = 'resnet'
        self.transform = data_transforms[mode][arch]
        with open(annotations_file, 'r') as f:
            self.tracklet_labels = json.load(f)
        tracklets = self.tracklet_labels.keys()
        self.image_paths = []
        for track in tracklets:
            tracklet_dir = os.path.join(parent_dir, track)
            images = os.listdir(tracklet_dir)
            for im in images:
                label = int(self.tracklet_labels[track])
                label = 1 if label > 0 else 0
                self.image_paths.append([os.path.join(tracklet_dir, im), track, label])

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path, track, label = self.image_paths[idx]
        image = Image.open(img_path).convert('RGB')
        if self.transform:
            image = self.transform(image)

        return image, track, label


class JerseyNumberLegibilityDataset(Dataset):
    def __init__(self, annotations_file, img_dir, mode='train', isBalanced=False, arch='resnet18'):
        if 'resnet' in arch:
            arch = 'resnet'
        self.transform = data_transforms[mode][arch]
        self.img_labels = pd.read_csv(annotations_file)
        if isBalanced:
            legible = self.img_labels[self.img_labels.iloc[:,1]==1]
            count_legible = len(legible)
            illegible = self.img_labels[self.img_labels.iloc[:,1]==0]
            print(count_legible, len(illegible))
            if len(illegible) > count_legible:
                illegible = illegible.sample(n=count_legible)
            self.img_labels = pd.concat([legible, illegible])
            print(f"Balanced dataset: legibles = {count_legible} all = {len(self.img_labels)}")
        else:
            legible = self.img_labels[self.img_labels.iloc[:, 1] == 1]
            count_legible = len(legible)
            print(f"As-is dataset: legibles = {count_legible} all = {len(self.img_labels)}")

        self.img_dir = img_dir

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.img_labels.iloc[idx, 0])
        image = Image.open(img_path).convert('RGB')
        label = self.img_labels.iloc[idx, 1]
        if self.transform:
            image = self.transform(image)

        return image, label, self.img_labels.iloc[idx, 0]
