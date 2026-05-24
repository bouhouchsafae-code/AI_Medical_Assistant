import os

import pandas as pd

import pydicom

import numpy as np

from PIL import Image

from tqdm import tqdm

# =========================
# 📁 PATHS
# =========================

CSV_PATH = "data/rsna/stage_2_train_labels.csv"

DICOM_DIR = "data/rsna/images"

OUTPUT_DIR = "data/rsna_processed"

# =========================
# 📁 CREATE FOLDERS
# =========================

NORMAL_DIR = os.path.join(

    OUTPUT_DIR,

    "NORMAL"

)

PNEUMONIA_DIR = os.path.join(

    OUTPUT_DIR,

    "PNEUMONIA"

)

os.makedirs(

    NORMAL_DIR,

    exist_ok=True

)

os.makedirs(

    PNEUMONIA_DIR,

    exist_ok=True

)

# =========================
# 📄 LOAD CSV
# =========================

df = pd.read_csv(

    CSV_PATH

)

# =========================
# 🧠 GROUP LABELS
# =========================

patient_labels = {}

for _, row in df.iterrows():

    patient_id = row["patientId"]

    target = row["Target"]

    if patient_id not in patient_labels:

        patient_labels[patient_id] = target

    else:

        patient_labels[patient_id] = max(

            patient_labels[patient_id],

            target

        )

# =========================
# 🔥 PROCESS IMAGES
# =========================

print("\nProcessing RSNA dataset...\n")

for patient_id, target in tqdm(

    patient_labels.items()

):

    dicom_path = os.path.join(

        DICOM_DIR,

        f"{patient_id}.dcm"

    )

    try:

        dicom = pydicom.dcmread(

            dicom_path

        )

        image = dicom.pixel_array

        # =========================
        # 📊 NORMALIZE
        # =========================

        image = image.astype(np.float32)

        image = (

            image - image.min()

        ) / (

            image.max() - image.min()

        )

        image = (image * 255).astype(

            np.uint8

        )

        # =========================
        # 🖼️ PIL IMAGE
        # =========================

        image = Image.fromarray(

            image

        ).convert("RGB")

        # =========================
        # 📏 RESIZE
        # =========================

        image = image.resize(

            (224, 224)

        )

        # =========================
        # 📁 SAVE
        # =========================

        if target == 1:

            save_path = os.path.join(

                PNEUMONIA_DIR,

                f"{patient_id}.png"

            )

        else:

            save_path = os.path.join(

                NORMAL_DIR,

                f"{patient_id}.png"

            )

        image.save(save_path)

    except Exception as e:

        print(

            f"Error with {patient_id}:",

            e

        )

print("\n✅ RSNA preprocessing complete!")