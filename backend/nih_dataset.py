import os

import pandas as pd

from PIL import Image

import torch

from torch.utils.data import Dataset
from torch.utils.data import DataLoader

from torchvision import transforms

# =========================
# 🏥 DISEASES
# =========================

DISEASES = [

    "Pneumonia",

    "Effusion",

    "Atelectasis",

    "Cardiomegaly",

    "Infiltration"

]

# =========================
# 🔥 TRANSFORMS
# =========================

transform = transforms.Compose([

    transforms.Resize((224, 224)),

    transforms.RandomHorizontalFlip(),

    transforms.RandomRotation(10),

    transforms.ToTensor(),

    transforms.Normalize(

        mean=[0.485, 0.456, 0.406],

        std=[0.229, 0.224, 0.225]

    )

])

# =========================
# 📦 NIH DATASET
# =========================

class NIHChestDataset(Dataset):

    def __init__(

        self,

        csv_file,

        image_dir,

        transform=None

    ):

        self.data = pd.read_csv(csv_file)

        self.image_dir = image_dir

        self.transform = transform

        # =========================
        # 🔥 KEEP ONLY NEEDED
        # =========================

        self.data = self.data[

            self.data["Finding Labels"]

            .apply(

                lambda x:

                any(

                    disease in x

                    for disease in DISEASES

                )

                or

                x == "No Finding"

            )

        ]

    # =========================
    # 📏 LEN
    # =========================

    def __len__(self):

        return len(self.data)

    # =========================
    # 📸 GET ITEM
    # =========================

    def __getitem__(self, idx):

        row = self.data.iloc[idx]

        image_name = row["Image Index"]

        labels = row["Finding Labels"]

        image_path = os.path.join(

            self.image_dir,

            image_name

        )

        image = Image.open(

            image_path

        ).convert("RGB")

        # =========================
        # 🏷️ MULTI LABEL
        # =========================

        target = torch.zeros(

            len(DISEASES)

        )

        for i, disease in enumerate(DISEASES):

            if disease in labels:

                target[i] = 1

        # =========================
        # 🔥 TRANSFORM
        # =========================

        if self.transform:

            image = self.transform(image)

        return image, target

# =========================
# 📁 PATHS
# =========================

csv_path = "data/nih14/Data_Entry_2017.csv"

image_dir = "data/nih14/images"

# =========================
# 📦 DATASET
# =========================

dataset = NIHChestDataset(

    csv_path,

    image_dir,

    transform=transform

)

# =========================
# 🔀 SPLIT
# =========================

train_size = int(

    0.8 * len(dataset)

)

test_size = len(dataset) - train_size

train_dataset, test_dataset = torch.utils.data.random_split(

    dataset,

    [train_size, test_size]

)

# =========================
# 📦 LOADERS
# =========================

train_loader = DataLoader(

    train_dataset,

    batch_size=16,

    shuffle=True

)

test_loader = DataLoader(

    test_dataset,

    batch_size=16,

    shuffle=False

)

# =========================
# ✅ INFO
# =========================

print(

    "NIH14 Dataset Loaded ✅"

)

print(

    "Total Images:",

    len(dataset)

)

print(

    "Diseases:",

    DISEASES

)