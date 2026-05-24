import sys
import os
import numpy as np

# =========================
# 🔧 Add project root
# =========================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.append(BASE_DIR)

# =========================
# 📦 Imports
# =========================

from backend.model import MedicalResNetModel

from backend.ai.gradcam import GradCAM

import torch

# =========================
# 🧠 Agent 1 — Classifier
# =========================

class MedicalClassifierAgent:

    def __init__(self):

        # =========================
        # 📁 Model path
        # =========================

        model_path = "models/best_resnet_model.pth"

        # =========================
        # ⚙️ Device
        # =========================

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        # =========================
        # 🧠 Load model
        # =========================

        self.model = MedicalResNetModel().to(
            self.device
        )

        # =========================
        # 💾 Load weights
        # =========================

        self.model.load_state_dict(
            torch.load(
                model_path,
                map_location=self.device
            )
        )

        self.model.eval()

        # =========================
        # 🔥 GradCAM
        # =========================

        self.gradcam = GradCAM(self.model)

    # =========================
    # 🚀 Prediction
    # =========================

    def predict(self, image):

        image = image.to(self.device)

        image = image.unsqueeze(0)

        with torch.no_grad():

            output = self.model(image)

            probs = torch.sigmoid(
                output
            )[0]

        

        predictions = []

        heatmaps = []

        # =========================
        # 🏥 MULTI LABEL
        # =========================
        prob = probs.item()

        predictions = []

        heatmaps = []

        if prob >= 0.25:

            predictions.append({

                "disease": "Pneumonia",

                "confidence": float(prob)

            })

            cam = self.gradcam.generate(

                image.squeeze(0),

                self.device

            )

            heatmaps.append({

                "disease": "Pneumonia",

                "cam": cam

            })

        return predictions, heatmaps
# =========================
# 🧠 Agent 2 — Explanation
# =========================

class ExplanationAgent:

    def explain(

        self,

        predictions

    ):

        # =========================
        # ✅ NO FINDING
        # =========================

        if len(predictions) == 0:

            return {

                "conditions": [

                    {

                        "condition":
                            "No Finding",

                        "severity":
                            "None",

                        "confidence":
                            0.99,

                        "description": (
                            "No abnormal "
                            "thoracic patterns "
                            "detected."
                        )

                    }

                ]

            }

        conditions = []

        for pred in predictions:

            prob = pred["confidence"]

            if prob > 0.85:

                severity = "High"

            elif prob > 0.6:

                severity = "Moderate"

            else:

                severity = "Low"

            conditions.append({

                "condition":
                    pred["disease"],

                "severity":
                    severity,

                "confidence":
                    prob,

                "description": (
                    f"The AI model "
                    f"detected radiological "
                    f"patterns consistent "
                    f"with "
                    f"{pred['disease']}."
                )

            })

        return {

            "conditions": conditions

        }

# =========================
# 🧠 Agent 3 — Report
# =========================

class ReportAgent:

    def generate(

        self,

        info

    ):

        report = """

==============================
      MEDICAL REPORT
==============================

"""

        for condition in info["conditions"]:

            report += f"""

Diagnosis:
{condition['condition']}

Severity:
{condition['severity']}

Confidence:
{condition['confidence']:.2f}

Details:
{condition['description']}

-----------------------------------

"""

        report += """

Recommendations:

- Clinical correlation recommended
- Additional imaging if necessary
- Follow-up with medical specialist
- Correlate with patient symptoms
- Perform further radiological evaluation if needed

⚠️ This system is an AI assistant
and does not replace a doctor.

"""

        return report

# =========================
# 🎯 ORCHESTRATOR
# =========================

class MedicalOrchestrator:

    def __init__(self):

        self.classifier = (
            MedicalClassifierAgent()
        )

        self.explainer = (
            ExplanationAgent()
        )

        self.reporter = (
            ReportAgent()
        )

    # =========================
    # 🚀 FULL PIPELINE
    # =========================

    def run(self, image):

        predictions, heatmaps = (
            self.classifier.predict(
                image
            )
        )

        info = self.explainer.explain(
            predictions
        )

        report = self.reporter.generate(
            info
        )

        return report, heatmaps

# =========================
# 🤖 Medical Chat Agent
# =========================

class MedicalChatAgent:

    def __init__(self):

        self.medical_keywords = [

            "pneumonia",
            "xray",
            "x-ray",
            "lung",
            "lungs",
            "doctor",
            "disease",
            "treatment",
            "symptoms",
            "infection",
            "radiology",
            "heatmap",
            "covid",
            "patient",
            "diagnosis",
            "medical",
            "medicine",
            "chest",
            "respiratory",
            "effusion",
            "atelectasis",
            "infiltration"

        ]

    def is_medical_question(
        self,
        message
    ):

        message = message.lower()

        return any(

            keyword in message

            for keyword
            in self.medical_keywords

        )

    def chat(self, message):

        if not self.is_medical_question(
            message
        ):

            return (
                "I am a medical AI assistant "
                "and can only answer "
                "medical-related questions."
            )

        return (
            "This appears to be a medical-related "
            "question. Further clinical evaluation "
            "by a healthcare professional "
            "is recommended."
        )