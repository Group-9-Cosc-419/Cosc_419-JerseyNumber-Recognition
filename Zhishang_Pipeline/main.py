import os
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import Dataset, DataLoader
from torchvision import models
from torchvision import transforms
from torchvision import datasets
from PIL import Image

K = 5

class LegibilityClassifier34(nn.Module):
    def __init__(self):
        super().__init__()
        self.model_ft = models.resnet34()
        num_ftrs = self.model_ft.fc.in_features
        self.model_ft.fc = nn.Linear(num_ftrs, 1)

    def forward(self, x):
        x = self.model_ft(x)
        x = F.sigmoid(x)
        return x

class MyDataset(Dataset):
    def __init__(self, root):
        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        self.image_paths = [
            os.path.join(root, f)
            for f in os.listdir(root)
            if f.lower().endswith('.jpg')
        ]

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        image = Image.open(img_path).convert('RGB')
        if self.transform:
            image = self.transform(image)

        return image


if __name__ == "__main__":
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    state_dict = torch.load("models/legibility_resnet34_soccer_20240215.pth", map_location="cpu")
    model = LegibilityClassifier34().to(device)
    model.load_state_dict(state_dict)
    del state_dict

    dataset = MyDataset("data/0")
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=len(dataset), shuffle=True)
    outputs = None
    for inputs in dataloader:
        inputs = inputs.to(device)
        with torch.no_grad():
            outputs = model(inputs)
        outputs = outputs.flatten()
        break
    
    y = None
    indeices = None
    if K <= len(dataset):
        y, indices = torch.topk(outputs, K, largest=True, sorted=True)
    print(y)
    print(indices)
