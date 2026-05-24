import sys
import os
import tempfile
from fastapi.responses import FileResponse
from auth.jwt_handler import (
    verify_token
)
from auth.auth_routes import (
    oauth2_scheme
)
from database.models import (
    Analysis,
    User
)

from pydantic import BaseModel

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)

sys.path.append(BASE_DIR)

from ai.pdf_generator import (
    generate_pdf
)
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../.."
        )
    )
)

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends
)

from sqlalchemy.orm import Session

from PIL import Image

import io
import numpy as np
import cv2
import tempfile

from torchvision import transforms

# =========================
# 🗄️ DATABASE
# =========================

from database.dependencies import (
    get_db
)

from database.models import (
    Analysis,
    User
)

# =========================
# 🔐 AUTH
# =========================

from auth.auth_routes import (
    oauth2_scheme
)

from auth.jwt_handler import (
    verify_token
)

# =========================
# ☁️ CLOUDINARY
# =========================

from services.cloudinary_service import (
    upload_image
)

# =========================
# 🤖 AI
# =========================

from ai.agents import (
    MedicalOrchestrator
)

# =========================
# 🚀 Router
# =========================

router = APIRouter()

# =========================
# 📄 PDF REQUEST
# =========================

class PDFRequest(BaseModel):

    report: str

# =========================
# 🤖 LOAD AI
# =========================

orchestrator = MedicalOrchestrator()

# =========================
# 🔄 IMAGE TRANSFORM
# =========================

transform = transforms.Compose([

    transforms.Resize((224, 224)),

    transforms.ToTensor()

])

# =========================
# 📤 ANALYZE API
# =========================

@router.post("/analyze")
async def analyze_image(

    patient_id: int,

    file: UploadFile = File(...),

    token: str = Depends(oauth2_scheme),

    db: Session = Depends(get_db)

):

    # =========================
    # 🔐 VERIFY TOKEN
    # =========================

    payload = verify_token(token)

    if payload is None:

        return {

            "success": False,
            "message": "Unauthorized"

        }

    # =========================
    # 👨‍⚕️ CURRENT DOCTOR
    # =========================

    doctor_email = payload["email"]

    doctor = db.query(User).filter(
        User.email == doctor_email
    ).first()

    if not doctor:

        return {

            "success": False,
            "message": "Doctor not found"

        }

    # =========================
    # 👤 GET PATIENT
    # =========================

    patient = db.query(User).filter(
        User.id == patient_id
    ).first()

    if not patient:

        return {

            "success": False,
            "message": "Patient not found"

        }

    # =========================
    # 🖼️ READ IMAGE
    # =========================

    image_bytes = await file.read()

    # =========================
    # ☁️ UPLOAD ORIGINAL IMAGE
    # =========================

    image_url = upload_image(

        io.BytesIO(image_bytes),

        folder="medical_ai/images"

    )

    # =========================
    # 🖼️ OPEN IMAGE
    # =========================

    image = Image.open(
        io.BytesIO(image_bytes)
    ).convert("RGB")

    # =========================
    # 🔄 TRANSFORM IMAGE
    # =========================

    img_tensor = transform(image)

    # =========================
    # 🤖 RUN AI
    # =========================

    report, heatmaps = orchestrator.run(
        img_tensor
    )

    # =========================
    # 🔥 MULTI HEATMAPS
    # =========================

    heatmap_urls = []

    original = cv2.cvtColor(

        np.array(image),

        cv2.COLOR_RGB2BGR

    )

    original = cv2.resize(

        original,

        (224, 224)

    )

    for item in heatmaps:

        disease = item["disease"]

        cam = item["cam"]

        # =========================
        # 🔥 CREATE HEATMAP
        # =========================

        heatmap = np.uint8(

            255 * cam

        )

        heatmap = cv2.applyColorMap(

            heatmap,

            cv2.COLORMAP_JET

        )

        superimposed = cv2.addWeighted(

            original,

            0.6,

            heatmap,

            0.4,

            0

        )

        # =========================
        # 💾 TEMP FILE
        # =========================

        temp_heatmap = tempfile.NamedTemporaryFile(

            suffix=".png",

            delete=False

        )

        cv2.imwrite(

            temp_heatmap.name,

            superimposed

        )

        # =========================
        # ☁️ UPLOAD
        # =========================

        heatmap_url = upload_image(

            temp_heatmap.name,

            folder="medical_ai/heatmaps"

        )

        heatmap_urls.append({

            "disease": disease,

            "url": heatmap_url

        })

    # =========================
    # 🧠 DIAGNOSIS
    # =========================

    diagnosis = report

    # =========================
    # 📊 CONFIDENCE
    # =========================

    confidence = 0.95

    # =========================
    # 💾 SAVE ANALYSIS
    # =========================

    analysis = Analysis(

        patient_id=patient.id,

        doctor_id=doctor.id,

        diagnosis=diagnosis,

        confidence=confidence,

        image_path=image_url,

        heatmap_path=heatmap_urls[0]["url"]
        if len(heatmap_urls) > 0
        else ""

    )

    db.add(analysis)

    db.commit()

    db.refresh(analysis)

    # =========================
    # ✅ RESPONSE
    # =========================

    return {

        "success": True,

        "analysis_id": analysis.id,

        "doctor": {

            "id": doctor.id,

            "first_name": doctor.first_name,

            "last_name": doctor.last_name,

            "email": doctor.email,

            "speciality": doctor.speciality

        },

        "patient": {

            "id": patient.id,

            "first_name": patient.first_name,

            "last_name": patient.last_name,

            "email": patient.email,

            "patient_number": patient.patient_number

        },

        "diagnosis": diagnosis,

        "confidence": confidence,

        "image_url": image_url,

        "heatmaps": heatmap_urls,

        "report": report

    }

# =========================
# 📜 ANALYSIS HISTORY
# =========================

@router.get("/analyses/history")
def get_analysis_history(

    token: str = Depends(oauth2_scheme),

    db: Session = Depends(get_db)

):

    # =========================
    # 🔐 VERIFY TOKEN
    # =========================

    payload = verify_token(token)

    if payload is None:

        return {

            "success": False,
            "message": "Unauthorized"

        }

    # =========================
    # 📜 GET ANALYSES
    # =========================

    analyses = db.query(
        Analysis
    ).all()

    # =========================
    # 📦 FORMAT RESULTS
    # =========================

    results = []

    for analysis in analyses:

        results.append({

            "id": analysis.id,

            "patient": {

                "id": analysis.patient.id,

                "first_name": analysis.patient.first_name,

                "last_name": analysis.patient.last_name,

                "email": analysis.patient.email,

                "phone": analysis.patient.phone,

                "patient_number":
                    analysis.patient.patient_number

            },

            "doctor": {

                "id": analysis.doctor.id,

                "first_name": analysis.doctor.first_name,

                "last_name": analysis.doctor.last_name,

                "email": analysis.doctor.email,

                "phone": analysis.doctor.phone,

                "speciality":
                    analysis.doctor.speciality

            },

            "diagnosis": analysis.diagnosis,

            "confidence": analysis.confidence,

            "image_url": analysis.image_path,

            "heatmap_url": analysis.heatmap_path,

            "created_at": analysis.created_at

        })

    # =========================
    # ✅ RESPONSE
    # =========================

    return {

        "success": True,

        "total_analyses": len(results),

        "analyses": results

    }

# =========================
# ❌ DELETE ANALYSIS
# =========================
# =========================
# 👤 PATIENT DETAILS
# =========================

@router.get("/doctor/patient/{patient_id}")
def get_patient_details(

    patient_id: int,

    token: str = Depends(oauth2_scheme),

    db: Session = Depends(get_db)

):

    # =========================
    # 🔐 VERIFY TOKEN
    # =========================

    payload = verify_token(token)

    if payload is None:

        return {

            "success": False,

            "message": "Unauthorized"

        }

    # =========================
    # 👨‍⚕️ GET DOCTOR
    # =========================

    doctor = db.query(User).filter(

        User.email == payload["email"]

    ).first()

    if not doctor:

        return {

            "success": False,

            "message": "Doctor not found"

        }

    # =========================
    # 👤 GET PATIENT
    # =========================

    patient = db.query(User).filter(

        User.id == patient_id,

        User.role == "patient",

        User.assigned_doctor_id == doctor.id

    ).first()

    if not patient:

        return {

            "success": False,

            "message": "Patient not found"

        }

    # =========================
    # 📜 GET ANALYSES
    # =========================

    analyses = db.query(Analysis).filter(

        Analysis.patient_id == patient.id,

        Analysis.doctor_id == doctor.id

    ).order_by(

        Analysis.created_at.desc()

    ).all()

    # =========================
    # 📦 FORMAT ANALYSES
    # =========================

    results = []

    for analysis in analyses:

        results.append({

            "id": analysis.id,

            "diagnosis": analysis.diagnosis,

            "confidence": analysis.confidence,

            "image_url": analysis.image_path,

            "heatmap_url": analysis.heatmap_path,

            "created_at": analysis.created_at

        })

    # =========================
    # ✅ RESPONSE
    # =========================

    return {

        "success": True,

        "patient": {

            "id": patient.id,

            "first_name": patient.first_name,

            "last_name": patient.last_name,

            "age": patient.age,

            "phone": patient.phone,

            "email": patient.email,

            "patient_number":
                patient.patient_number

        },
        "doctor": {

            "first_name": doctor.first_name,

            "last_name": doctor.last_name,

            "email": doctor.email,

            "speciality": doctor.speciality

        },

        "total_analyses": len(results),

        "analyses": results

    }

@router.delete("/analysis/{analysis_id}")
def delete_analysis(

    analysis_id: int,

    token: str = Depends(oauth2_scheme),

    db: Session = Depends(get_db)

):

    # =========================
    # 🔐 VERIFY TOKEN
    # =========================

    payload = verify_token(token)

    if payload is None:

        return {

            "success": False,

            "message": "Unauthorized"

        }

    # =========================
    # 🔎 FIND ANALYSIS
    # =========================

    analysis = db.query(Analysis).filter(

        Analysis.id == analysis_id

    ).first()

    # =========================
    # ❌ NOT FOUND
    # =========================

    if not analysis:

        return {

            "success": False,

            "message": "Analysis not found"

        }

    # =========================
    # 🗑️ DELETE
    # =========================

    db.delete(analysis)

    db.commit()

    # =========================
    # ✅ RESPONSE
    # =========================

    return {

        "success": True,

        "message": f"Analysis {analysis_id} deleted successfully"

    }
# =========================
# 📄 GENERATE PDF
# =========================

@router.post("/generate-pdf")
def generate_medical_pdf(

    data: PDFRequest

):

    # =========================
    # 📄 GENERATE PDF FILE
    # =========================

    filename = generate_pdf(

        data.report,

        filename="medical_report.pdf"

    )

    # =========================
    # 📥 RETURN FILE
    # =========================

    return FileResponse(

        path=filename,

        media_type="application/pdf",

        filename="medical_report.pdf"

    )
# =========================
# 👤 MY ANALYSES
# =========================

@router.get("/my-analyses")

def my_analyses(

    token: str = Depends(

        oauth2_scheme

    ),

    db: Session = Depends(get_db)

):

    # =========================
    # 🔐 VERIFY TOKEN
    # =========================

    payload = verify_token(token)

    if payload is None:

        return {

            "success": False,

            "message": "Unauthorized"

        }

    # =========================
    # 👤 FIND USER
    # =========================

    user = db.query(User).filter(

        User.email == payload["email"]

    ).first()

    if not user:

        return {

            "success": False,

            "message": "User not found"

        }

    # =========================
    # 📦 GET ANALYSES
    # =========================

    analyses = db.query(Analysis).filter(

        Analysis.patient_id == user.id

    ).order_by(

        Analysis.created_at.desc()

    ).all()

    # =========================
    # 📄 FORMAT RESPONSE
    # =========================

    formatted = []

    for item in analyses:

        formatted.append({

            "id": item.id,

            "diagnosis": item.diagnosis,

            "confidence": item.confidence,

            "report": item.report,

            "image_url": item.image_path,

            "pdf_url": item.pdf_path,

            "created_at": str(

                item.created_at

            )

        })

    return {

        "success": True,

        "analyses": formatted

    }