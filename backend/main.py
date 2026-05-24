from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware
)

from routes.analysis_routes import (
    router as analysis_router
)

from auth.auth_routes import (
    router as auth_router
)

from routes.doctor_routes import (
    router as doctor_router
)

from routes.ai_routes import (
    router as ai_router
)
from routes.chat_routes import (
    router as chat_router
)
# =========================
# 🗄️ DATABASE
# =========================

from database.database import (
    engine
)

from database.models import (
    Base
)

# =========================
# 🧱 CREATE DATABASE
# =========================

Base.metadata.create_all(
    bind=engine
)

# =========================
# 🚀 FastAPI APP
# =========================

app = FastAPI(

    title="AI Medical Assistant API"

)

# =========================
# 🌐 CORS
# =========================

app.add_middleware(

    CORSMiddleware,

    allow_origins=[

        "http://localhost:3000"

    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)

# =========================
# 📌 ROUTES
# =========================

app.include_router(
    analysis_router
)

app.include_router(
    auth_router
)

app.include_router(
    doctor_router
)

app.include_router(
    ai_router
)
app.include_router(
    chat_router
)

# =========================
# 🏠 HOME
# =========================

@app.get("/")
def home():

    return {

        "message": "AI Medical Assistant API running"

    }