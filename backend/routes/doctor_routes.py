from fastapi import APIRouter, Depends

from pydantic import BaseModel

from sqlalchemy.orm import Session

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

from auth.password_handler import (
    hash_password
)

# =========================
# 🚀 ROUTER
# =========================

router = APIRouter(

    prefix="/doctor",

    tags=["Doctor"]

)

# =========================
# ➕ ADD PATIENT SCHEMA
# =========================

class AddPatientRequest(BaseModel):

    username: str

    first_name: str

    last_name: str

    age: int

    phone: str

    email: str

    password: str


# =========================
# ➕ ADD PATIENT
# =========================

@router.post("/add-patient")
def add_patient(

    data: AddPatientRequest,

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
    # 📧 CHECK EMAIL
    # =========================

    existing_user = db.query(User).filter(

        User.email == data.email

    ).first()

    if existing_user:

        return {

            "success": False,

            "message": "Email already exists"

        }

    # =========================
    # 🔒 HASH PASSWORD
    # =========================

    hashed_password = hash_password(
        data.password
    )
    # =========================
    # 🔢 GENERATE PATIENT NUMBER
    # =========================

    doctor_patients_count = db.query(User).filter(

        User.role == "patient",

        User.assigned_doctor_id == doctor.id

    ).count()

    new_patient_number = (
        f"PAT-{doctor_patients_count + 1:03d}"
    )

    # =========================
    # 👤 CREATE PATIENT
    # =========================

    patient = User(

        username=data.username,

        first_name=data.first_name,

        last_name=data.last_name,

        age=data.age,

        phone=data.phone,

        email=data.email,

        password=hashed_password,

        role="patient",

        patient_number=new_patient_number,
        
        assigned_doctor_id=doctor.id

    )

    # =========================
    # 💾 SAVE
    # =========================

    db.add(patient)

    db.commit()

    db.refresh(patient)

    # =========================
    # ✅ RESPONSE
    # =========================

    return {

        "success": True,

        "message": "Patient added successfully",

        "patient": {

            "id": patient.id,

            "first_name": patient.first_name,

            "last_name": patient.last_name,

            "email": patient.email,

            "patient_number": patient.patient_number

        }

    }

# =========================
# 📊 DASHBOARD STATS
# =========================

@router.get("/dashboard/stats")
def dashboard_stats(

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

    # =========================
    # 👨‍⚕️ GET DOCTOR
    # =========================

    doctor = db.query(User).filter(

        User.email == doctor_email

    ).first()

    if not doctor:

        return {

            "success": False,

            "message": "Doctor not found"

        }

    # =========================
    # 📊 GET ANALYSES
    # =========================

    analyses = db.query(Analysis).filter(

        Analysis.doctor_id == doctor.id

    ).all()

    # =========================
    # 👥 TOTAL PATIENTS
    # =========================

    total_patients = db.query(User).filter(

        User.assigned_doctor_id == doctor.id,

        User.role == "patient"

    ).count()

    # =========================
    # 📄 TOTAL REPORTS
    # =========================

    reports_generated = len(
        analyses
    )

    # =========================
    # 🦠 PNEUMONIA CASES
    # =========================

    pneumonia_cases = len([

        analysis
        for analysis in analyses

        if analysis.diagnosis
        == "Pneumonia"

    ])

    # =========================
    # ✅ RESPONSE
    # =========================

    return {

        "success": True,

        "stats": {

            "total_patients":
                total_patients,

            "reports_generated":
                reports_generated,

            "pneumonia_cases":
                pneumonia_cases

        }

    }

# =========================
# 👥 GET PATIENTS
# =========================

@router.get("/patients")
def get_patients(

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
    # 👥 GET DOCTOR PATIENTS
    # =========================

    patients = db.query(User).filter(

        User.role == "patient",

        User.assigned_doctor_id == doctor.id

    ).all()

    # =========================
    # 📦 FORMAT RESULTS
    # =========================

    results = []

    for patient in patients:

        results.append({

            "id": patient.id,

            "first_name": patient.first_name,

            "last_name": patient.last_name,

            "email": patient.email,

            "phone": patient.phone,

            "patient_number":
                patient.patient_number

        })

    # =========================
    # ✅ RESPONSE
    # =========================

    return {

        "success": True,

        "patients": results

    }