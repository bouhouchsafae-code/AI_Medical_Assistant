from rsna_dataset import (
    train_loader,
    test_loader
)

from model import PneumoniaModel

import torch

import torch.nn as nn

import torch.optim as optim

from tqdm import tqdm

import json

from sklearn.metrics import (

    precision_score,

    recall_score,

    f1_score

)

# =========================
# 🔥 FOCAL LOSS
# =========================

class FocalLoss(nn.Module):

    def __init__(

        self,

        alpha=1,

        gamma=2

    ):

        super(FocalLoss, self).__init__()

        self.alpha = alpha

        self.gamma = gamma

        self.bce = nn.BCEWithLogitsLoss(

            reduction="none"

        )

    def forward(

        self,

        inputs,

        targets

    ):

        bce_loss = self.bce(

            inputs,

            targets

        )

        probs = torch.sigmoid(inputs)

        pt = torch.where(

            targets == 1,

            probs,

            1 - probs

        )

        focal_loss = (

            self.alpha
            *
            (1 - pt) ** self.gamma
            *
            bce_loss

        )

        return focal_loss.mean()

# =========================
# 🚀 MAIN
# =========================

def main():

    print(

        "Starting RSNA Pneumonia Training..."

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
    # 🧠 MODEL
    # =========================

    model = PneumoniaModel().to(device)

    # =========================
    # 🔥 LOSS
    # =========================

    criterion = FocalLoss(

        alpha=1,

        gamma=2

    )

    # =========================
    # ⚙️ OPTIMIZER
    # =========================

    optimizer = optim.Adam(

        model.parameters(),

        lr=0.00003,

        weight_decay=1e-4

    )

    # =========================
    # 📉 SCHEDULER
    # =========================

    scheduler = optim.lr_scheduler.CosineAnnealingLR(

        optimizer,

        T_max=50

    )

    # =========================
    # 🔧 CONFIG
    # =========================

    epochs = 50

    best_recall = 0

    patience = 15

    counter = 0

    threshold = 0.25

    # =========================
    # 📊 TRACKING
    # =========================

    train_losses = []

    val_accuracies = []

    # =========================
    # 🔥 TRAIN LOOP
    # =========================

    for epoch in range(epochs):

        model.train()

        total_loss = 0

        loop = tqdm(

            train_loader,

            desc=f"Epoch {epoch+1}/{epochs}"

        )

        # =========================
        # 🚀 TRAINING
        # =========================

        for images, labels in loop:

            images = images.to(device)

            labels = labels.float().unsqueeze(1).to(device)

            outputs = model(images)

            loss = criterion(

                outputs,

                labels

            )

            optimizer.zero_grad()

            loss.backward()

            optimizer.step()

            total_loss += loss.item()

            loop.set_postfix(

                loss=f"{loss.item():.4f}"

            )

        print(

            f"\nEpoch {epoch+1} "

            f"completed | "

            f"Loss: {total_loss:.4f}"

        )

        # =========================
        # 🧪 VALIDATION
        # =========================

        model.eval()

        correct = 0

        total = 0

        all_preds = []

        all_labels = []

        with torch.no_grad():

            for images, labels in test_loader:

                images = images.to(device)

                labels = labels.float().unsqueeze(1).to(device)

                outputs = model(images)

                preds = (

                    torch.sigmoid(outputs)

                    > threshold

                ).float()

                correct += (

                    preds == labels

                ).sum().item()

                total += labels.numel()

                all_preds.extend(

                    preds.cpu()

                    .numpy()

                    .reshape(-1)

                )

                all_labels.extend(

                    labels.cpu()

                    .numpy()

                    .reshape(-1)

                )

        # =========================
        # 📊 METRICS
        # =========================

        accuracy = correct / total

        precision = precision_score(

            all_labels,

            all_preds,

            zero_division=0

        )

        recall = recall_score(

            all_labels,

            all_preds,

            zero_division=0

        )

        f1 = f1_score(

            all_labels,

            all_preds,

            zero_division=0

        )

        print(

            f"""

==============================
     VALIDATION METRICS
==============================

Accuracy : {accuracy:.4f}

Precision: {precision:.4f}

Recall   : {recall:.4f}

F1 Score : {f1:.4f}

==============================

"""
        )

        # =========================
        # 📉 SCHEDULER
        # =========================

        scheduler.step()
        # =========================
        # 📊 SAVE HISTORY
        # =========================

        train_losses.append(total_loss)

        val_accuracies.append(accuracy)

        # =========================
        # 💾 SAVE BEST MODEL
        # =========================

        if recall > best_recall:

            best_recall = recall

            torch.save(

                model.state_dict(),

                "best_pneumonia_model.pth"

            )

            print(

                "🔥 Best model saved!"

            )

            counter = 0

        else:

            counter += 1

        # =========================
        # ⛔ EARLY STOPPING
        # =========================

        #if counter >= patience:

         #   print(

          #      "⛔ Early stopping triggered"

           # )

            #break

    # =========================
    # 🏁 FINAL RESULT
    # =========================

    print(

        f"\n🔥 BEST RECALL: "

        f"{best_recall:.4f}"

    )

    # =========================
    # 💾 SAVE HISTORY
    # =========================

    with open(

        "training_history.json",

        "w"

    ) as f:

        json.dump({

            "loss": train_losses,

            "accuracy": val_accuracies

        }, f)

    print(

        "Training history saved ✅"

    )

# =========================
# 🚀 START
# =========================

if __name__ == "__main__":

    main()