from sqlalchemy import (

    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Boolean
)

from sqlalchemy.orm import (
    relationship
)

from datetime import datetime

from database.database import Base

# =========================
# 👤 USER MODEL
# =========================

class User(Base):

    __tablename__ = "users"

    # =========================
    # 🆔 ID
    # =========================

    id = Column(

        Integer,

        primary_key=True,

        index=True

    )

    # =========================
    # 👤 BASIC INFO
    # =========================

    username = Column(

        String,

        nullable=False

    )

    first_name = Column(

        String,

        nullable=True

    )

    last_name = Column(

        String,

        nullable=True

    )

    age = Column(

        Integer,

        nullable=True

    )

    phone = Column(

        String,

        nullable=True

    )

    email = Column(

        String,

        unique=True,

        nullable=False

    )

    password = Column(

        String,

        nullable=False

    )

    # =========================
    # 🩺 ROLE
    # =========================

    role = Column(

        String,

        default="patient"

    )

    # =========================
    # 👨‍⚕️ ASSIGNED DOCTOR
    # =========================

    assigned_doctor_id = Column(

        Integer,

        ForeignKey("users.id"),

        nullable=True

    )

    # =========================
    # 🏥 DOCTOR SPECIALITY
    # =========================

    speciality = Column(

        String,

        nullable=True

    )

    # =========================
    # 🆔 PATIENT NUMBER
    # =========================

    patient_number = Column(

        String,

        unique=True,

        nullable=True

    )

    # =========================
    # 👨‍⚕️ DOCTOR RELATIONSHIP
    # =========================

    assigned_doctor = relationship(

        "User",

        remote_side=[id],

        backref="assigned_patients"

    )

    # =========================
    # 📜 RELATIONSHIPS
    # =========================

    doctor_analyses = relationship(

        "Analysis",

        foreign_keys="Analysis.doctor_id",

        back_populates="doctor"

    )

    patient_analyses = relationship(

        "Analysis",

        foreign_keys="Analysis.patient_id",

        back_populates="patient"

    )

    must_change_password = Column(

        Boolean,

        default=True

    )

# =========================
# 📜 ANALYSIS MODEL
# =========================

class Analysis(Base):

    __tablename__ = "analyses"

    # =========================
    # 🆔 ID
    # =========================

    id = Column(

        Integer,

        primary_key=True,

        index=True

    )

    # =========================
    # 👤 PATIENT
    # =========================

    patient_id = Column(

        Integer,

        ForeignKey("users.id"),

        nullable=False

    )

    # =========================
    # 👨‍⚕️ DOCTOR
    # =========================

    doctor_id = Column(

        Integer,

        ForeignKey("users.id"),

        nullable=False

    )

    # =========================
    # 🧠 DIAGNOSIS
    # =========================

    diagnosis = Column(

        String,

        nullable=False

    )

    # =========================
    # 📊 CONFIDENCE
    # =========================

    confidence = Column(

        Float,

        nullable=False

    )

    # =========================
    # 🖼️ IMAGE URL
    # =========================

    image_path = Column(

        String,

        nullable=True

    )

    # =========================
    # 🔥 HEATMAP URL
    # =========================

    heatmap_path = Column(

        String,

        nullable=True

    )

    # =========================
    # 📅 CREATED AT
    # =========================

    created_at = Column(

        DateTime,

        default=datetime.utcnow

    )

    # =========================
    # 🔗 RELATIONSHIPS
    # =========================

    doctor = relationship(

        "User",

        foreign_keys=[doctor_id],

        back_populates="doctor_analyses"

    )

    patient = relationship(

        "User",

        foreign_keys=[patient_id],

        back_populates="patient_analyses"

    )
    # =========================
# 💬 CHAT MESSAGE
# =========================

class Message(Base):

    __tablename__ = "messages"

    id = Column(

        Integer,

        primary_key=True,

        index=True

    )

    sender_id = Column(

        Integer,

        ForeignKey("users.id")

    )

    receiver_id = Column(

        Integer,

        ForeignKey("users.id")

    )

    content = Column(

        String

    )

    created_at = Column(

        DateTime,

        default=datetime.utcnow

    )