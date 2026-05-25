import torch

import torch.nn as nn

import torch.optim as optim

from torchvision import datasets
from torchvision import transforms
from torchvision import models

from torch.utils.data import DataLoader

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

        mean=[0.485, 0.456, 0.406],

        std=[0.229, 0.224, 0.225]

    )

])

test_transform = transforms.Compose([

    transforms.Resize((224, 224)),

    transforms.ToTensor(),

    transforms.Normalize(

        mean=[0.485, 0.456, 0.406],

        std=[0.229, 0.224, 0.225]

    )

])

# =========================
# 📂 DATASETS
# =========================

train_dataset = datasets.ImageFolder(

    "chest_xray/train",

    transform=train_transform

)

test_dataset = datasets.ImageFolder(

    "chest_xray/test",

    transform=test_transform

)

# =========================
# 🚀 DATALOADERS
# =========================

train_loader = DataLoader(

    train_dataset,

    batch_size=32,

    shuffle=True

)

test_loader = DataLoader(

    test_dataset,

    batch_size=32,

    shuffle=False

)

# =========================
# ⚙️ DEVICE
# =========================

device = torch.device(

    "cuda"

    if torch.cuda.is_available()

    else "cpu"

)

print("Using device:", device)

# =========================
# 🧠 RESNET18
# =========================

model = models.resnet18(

    pretrained=True

)

# =========================
# 🔥 FINAL LAYER
# =========================

num_features = model.fc.in_features

model.fc = nn.Linear(

    num_features,

    1

)

model = model.to(device)

# =========================
# 🔥 LOSS
# =========================

criterion = nn.BCEWithLogitsLoss()

# =========================
# ⚙️ OPTIMIZER
# =========================

optimizer = optim.Adam(

    model.parameters(),

    lr=0.0001

)

# =========================
# 🔥 TRAINING
# =========================

epochs = 30

best_accuracy = 0

for epoch in range(epochs):

    model.train()

    running_loss = 0

    correct = 0

    total = 0

    for images, labels in train_loader:

        images = images.to(device)

        labels = (

            labels.float()

            .unsqueeze(1)

            .to(device)

        )

        outputs = model(images)

        loss = criterion(

            outputs,

            labels

        )

        optimizer.zero_grad()

        loss.backward()

        optimizer.step()

        running_loss += loss.item()

        preds = (

            torch.sigmoid(outputs)

            > 0.5

        ).float()

        correct += (

            preds == labels

        ).sum().item()

        total += labels.size(0)

    train_acc = correct / total

    print(

        f"Epoch [{epoch+1}/{epochs}] "

        f"Loss: {running_loss:.4f} "

        f"Accuracy: {train_acc:.4f}"

    )

    # =========================
    # 🧪 EVALUATION
    # =========================

    model.eval()

    correct = 0

    total = 0

    with torch.no_grad():

        for images, labels in test_loader:

            images = images.to(device)

            labels = (

                labels.float()

                .unsqueeze(1)

                .to(device)

            )

            outputs = model(images)

            preds = (

                torch.sigmoid(outputs)

                > 0.5

            ).float()

            correct += (

                preds == labels

            ).sum().item()

            total += labels.size(0)

    accuracy = correct / total

    print(

        f"Test Accuracy: {accuracy:.4f}"

    )

    # =========================
    # 💾 SAVE BEST MODEL
    # =========================

    if accuracy > best_accuracy:

        best_accuracy = accuracy

        torch.save(

            model.state_dict(),

            "best_resnet_model.pth"

        )

        print(

            "🔥 Best model saved!"
        )

print(

    f"\nBest Accuracy: {best_accuracy:.4f}"
)