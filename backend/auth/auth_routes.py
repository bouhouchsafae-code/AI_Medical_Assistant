from fastapi import APIRouter, Depends

from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm
)

from pydantic import BaseModel

from sqlalchemy.orm import Session

# =========================
# 🔐 AUTH
# =========================

from auth.password_handler import (
    hash_password,
    verify_password
)

from auth.jwt_handler import (
    create_access_token,
    verify_token
)

# =========================
# 🗄️ DATABASE
# =========================

from database.dependencies import (
    get_db
)

from database.models import (
    User
)

# =========================
# 🚀 ROUTER
# =========================

router = APIRouter()

# =========================
# 🔐 OAuth2 Scheme
# =========================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token"
)

# =========================
# 🧠 REGISTER SCHEMA
# =========================

class RegisterRequest(BaseModel):

    username: str

    first_name: str

    last_name: str

    age: int

    phone: str

    email: str

    password: str

    role: str

    speciality: str | None = None

    patient_number: str | None = None

    assigned_doctor_id: int | None = None

# =========================
# 📝 REGISTER
# =========================

@router.post("/register")
def register(

    data: RegisterRequest,

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
    # 👨‍⚕️ CURRENT DOCTOR
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
    # CHECK EXISTING EMAIL
    # =========================

    existing_user = db.query(User).filter(
        User.email == data.email
    ).first()

    # =========================
    # EMAIL EXISTS
    # =========================

    if existing_user:

        return {

            "success": False,

            "message": "Email already exists"

        }

    # =========================
    # HASH PASSWORD
    # =========================

    hashed_password = hash_password(
        data.password
    )

    # =========================
    # CREATE USER
    # =========================

    new_user = User(

        username=data.username,

        first_name=data.first_name,

        last_name=data.last_name,

        age=data.age,

        phone=data.phone,

        email=data.email,

        password=hashed_password,

        role=data.role.lower(),

        speciality=data.speciality,

        patient_number=data.patient_number,

        must_change_password=(data.role.lower() == "patient"),

        assigned_doctor_id=doctor.id,

    )

    # =========================
    # SAVE USER
    # =========================

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    # =========================
    # CREATE TOKEN
    # =========================

    token = create_access_token({

        "email": new_user.email,

        "role": new_user.role

    })

    # =========================
    # RESPONSE
    # =========================

    return {

        "success": True,

        "message": "User registered successfully",

        "token": token

    }

# =========================
# 🔓 SWAGGER LOGIN
# =========================

@router.post("/token")
def login(

    form_data: OAuth2PasswordRequestForm = Depends(),

    db: Session = Depends(get_db)

):

    # =========================
    # FIND USER
    # =========================

    user_found = db.query(User).filter(

        User.email == form_data.username

    ).first()

    # =========================
    # INVALID EMAIL
    # =========================

    if not user_found:

        return {

            "success": False,

            "message": "Invalid email"

        }

    # =========================
    # VERIFY PASSWORD
    # =========================

    valid_password = verify_password(

        form_data.password,

        user_found.password

    )

    # =========================
    # INVALID PASSWORD
    # =========================

    if not valid_password:

        return {

            "success": False,

            "message": "Invalid password"

        }

    # =========================
    # GENERATE TOKEN
    # =========================

    token = create_access_token({

        "email": user_found.email,

        "role": user_found.role

    })

    # =========================
    # RESPONSE
    # =========================

    return {

        "access_token": token,

        "token_type": "bearer"

    }

# =========================
# 🔓 FRONTEND LOGIN
# =========================

class LoginRequest(BaseModel):

    email: str

    password: str

@router.post("/login")
def frontend_login(

    data: LoginRequest,

    db: Session = Depends(get_db)

):

    # =========================
    # FIND USER
    # =========================

    user_found = db.query(User).filter(

        User.email == data.email

    ).first()

    # =========================
    # INVALID EMAIL
    # =========================

    if not user_found:

        return {

            "success": False,

            "message": "Invalid email"

        }

    # =========================
    # VERIFY PASSWORD
    # =========================

    valid_password = verify_password(

        data.password,

        user_found.password

    )

    # =========================
    # INVALID PASSWORD
    # =========================

    if not valid_password:

        return {

            "success": False,

            "message": "Invalid password"

        }

    # =========================
    # GENERATE TOKEN
    # =========================

    token = create_access_token({

        "email": user_found.email,

        "role": user_found.role

    })

    # =========================
    # RESPONSE
    # =========================

    return {

        "success": True,

        "access_token": token,

        "token_type": "bearer",

        "user": {

            "id": user_found.id,

            "username": user_found.username,

            "first_name": user_found.first_name,

            "last_name": user_found.last_name,

            "age": user_found.age,

            "phone": user_found.phone,

            "email": user_found.email,

            "role": user_found.role,

            "speciality": user_found.speciality,

            "patient_number": user_found.patient_number,

            "must_change_password": user_found.must_change_password,

            "assigned_doctor_id": user_found.assigned_doctor_id,

        }

    }

# =========================
# 👤 PROFILE
# =========================

@router.get("/profile")
def profile(

    token: str = Depends(oauth2_scheme),

    db: Session = Depends(get_db)

):

    # =========================
    # VERIFY TOKEN
    # =========================

    payload = verify_token(token)

    # =========================
    # UNAUTHORIZED
    # =========================

    if payload is None:

        return {

            "success": False,

            "message": "Unauthorized"

        }

    # =========================
    # GET USER
    # =========================

    user = db.query(User).filter(
        User.email == payload["email"]
    ).first()

    # =========================
    # USER NOT FOUND
    # =========================

    if not user:

        return {

            "success": False,

            "message": "User not found"

        }

    # =========================
    # RESPONSE
    # =========================

    return {

        "success": True,

        "user": {

            "id": user.id,

            "username": user.username,

            "first_name": user.first_name,

            "last_name": user.last_name,

            "age": user.age,

            "phone": user.phone,

            "email": user.email,

            "role": user.role,

            "speciality": user.speciality,

            "patient_number": user.patient_number

        }

    }
# =========================
# 🔐 CHANGE PASSWORD
# =========================

class ChangePasswordRequest(

    BaseModel

):

    new_password: str

@router.post("/change-password")

def change_password(

    data: ChangePasswordRequest,

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
    # 🔒 HASH PASSWORD
    # =========================

    hashed_password = hash_password(

        data.new_password

    )

    # =========================
    # 💾 UPDATE USER
    # =========================

    user.password = hashed_password

    user.must_change_password = False

    db.commit()

    # =========================
    # ✅ RESPONSE
    # =========================

    return {

        "success": True,

        "message": "Password updated"

    }

# =========================
# ❌ DELETE USER
# =========================

@router.delete("/delete-user/{user_id}")

def delete_user(

    user_id: int,

    db: Session = Depends(get_db)

):

    user = db.query(User).filter(

        User.id == user_id

    ).first()

    if not user:

        return {

            "success": False,

            "message": "User not found"

        }

    db.delete(user)

    db.commit()

    return {

        "success": True,

        "message": "User deleted"

    }