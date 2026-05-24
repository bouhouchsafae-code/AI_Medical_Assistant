from torchvision import datasets, transforms

from torch.utils.data import DataLoader

import torch

# =========================
# 🔥 TRAIN TRANSFORMS
# =========================

transform_train = transforms.Compose([

    # =========================
    # 📏 RESIZE
    # =========================

    transforms.Resize((224, 224)),

    # =========================
    # 🔄 DATA AUGMENTATION
    # =========================

    transforms.RandomHorizontalFlip(

        p=0.5

    ),

    transforms.RandomRotation(

        degrees=12

    ),

    transforms.RandomAffine(

        degrees=0,

        translate=(0.05, 0.05),

        scale=(0.95, 1.05)

    ),

    transforms.ColorJitter(

        brightness=0.15,

        contrast=0.15

    ),

    # =========================
    # 🔥 TENSOR
    # =========================

    transforms.ToTensor(),

    # =========================
    # 🧠 DENSENET NORMALIZATION
    # =========================

    transforms.Normalize(

        mean=[0.485, 0.456, 0.406],

        std=[0.229, 0.224, 0.225]

    )

])

# =========================
# 🧪 TEST TRANSFORMS
# =========================

transform_test = transforms.Compose([

    transforms.Resize((224, 224)),

    transforms.ToTensor(),

    transforms.Normalize(

        mean=[0.485, 0.456, 0.406],

        std=[0.229, 0.224, 0.225]

    )

])

# =========================
# 📁 DATASET PATHS
# =========================

train_path = "data/chest_xray/train"

test_path = "data/chest_xray/test"

# =========================
# 📦 LOAD DATASETS
# =========================

train_dataset = datasets.ImageFolder(

    train_path,

    transform=transform_train

)

test_dataset = datasets.ImageFolder(

    test_path,

    transform=transform_test

)

# =========================
# ⚖️ HANDLE CLASS IMBALANCE
# =========================

targets = [

    label

    for _, label

    in train_dataset

]

class_count = torch.bincount(

    torch.tensor(targets)

)

weights = 1. / class_count.float()

sample_weights = [

    weights[label]

    for label in targets

]

sampler = torch.utils.data.WeightedRandomSampler(

    sample_weights,

    num_samples=len(sample_weights),

    replacement=True

)

# =========================
# 📦 DATALOADERS
# =========================

train_loader = DataLoader(

    train_dataset,

    batch_size=32,

    sampler=sampler,

    num_workers=0

)

test_loader = DataLoader(

    test_dataset,

    batch_size=32,

    shuffle=False,

    num_workers=0

)

# =========================
# ✅ INFO
# =========================

print("Dataset loaded successfully ✅")

print(

    "Classes:",

    train_dataset.classes

)

print(

    "Class distribution:",

    class_count.tolist()

)