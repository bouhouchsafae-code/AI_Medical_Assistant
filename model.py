import torch.nn as nn

import torchvision.models as models

from torchvision.models import ResNet18_Weights

# =========================
# 🔥 MULTI-DISEASE RESNET
# =========================

class MedicalResNetModel(

    nn.Module

):

    def __init__(self):

        super(

            MedicalResNetModel,

            self

        ).__init__()

        # =========================
        # 🧠 RESNET50
        # =========================

        self.model = models.resnet18(

            weights=ResNet18_Weights.DEFAULT

        )

        # =========================
        # 🎯 CLASSIFIER
        # =========================

        in_features = (

            self.model.fc.in_features

        )

        self.model.fc = nn.Linear(

            in_features,

            1

        )

    # =========================
    # 🚀 FORWARD
    # =========================

    def forward(

        self,

        x

    ):

        return self.model(x)