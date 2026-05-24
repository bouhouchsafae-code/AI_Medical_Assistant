from torchvision import datasets

from torchvision import transforms

from torch.utils.data import DataLoader

from torch.utils.data import random_split

# =========================
# 🔥 TRANSFORMS
# =========================

train_transform = transforms.Compose([

    transforms.Resize((224, 224)),

    transforms.RandomHorizontalFlip(),

    transforms.RandomRotation(10),

    transforms.ColorJitter(

        brightness=0.1,

        contrast=0.1

    ),

    transforms.ToTensor(),

    transforms.Normalize(

        [0.485, 0.456, 0.406],

        [0.229, 0.224, 0.225]

    )

])

test_transform = transforms.Compose([

    transforms.Resize((224, 224)),

    transforms.ToTensor(),

    transforms.Normalize(

        [0.485, 0.456, 0.406],

        [0.229, 0.224, 0.225]

    )

])

# =========================
# 📁 DATASET
# =========================

dataset = datasets.ImageFolder(

    "data/rsna_processed",

    transform=train_transform

)

# =========================
# 📊 SPLIT
# =========================

train_size = int(

    0.8 * len(dataset)

)

test_size = len(dataset) - train_size

train_dataset, test_dataset = random_split(

    dataset,

    [train_size, test_size]

)

# =========================
# 🔥 TEST TRANSFORM
# =========================

test_dataset.dataset.transform = test_transform

# =========================
# 📦 DATALOADERS
# =========================

train_loader = DataLoader(

    train_dataset,

    batch_size=16,

    shuffle=True,

    num_workers=0

)

test_loader = DataLoader(

    test_dataset,

    batch_size=16,

    shuffle=False,

    num_workers=0

)

# =========================
# 📊 CLASSES
# =========================

classes = dataset.classes

print("\n✅ RSNA Dataset Loaded")

print("Classes:", classes)

print("Total Images:", len(dataset))