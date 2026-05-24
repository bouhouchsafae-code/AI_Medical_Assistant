from fastapi import APIRouter, Depends

from pydantic import BaseModel

from sqlalchemy.orm import Session

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
# 🗄️ DATABASE
# =========================

from database.dependencies import (
    get_db
)

from database.models import (
    User,
    Message
)

# =========================
# 🚀 ROUTER
# =========================

router = APIRouter()

# =========================
# 📩 SEND MESSAGE
# =========================

class MessageRequest(

    BaseModel

):

    receiver_id: int

    content: str

@router.post("/send-message")

def send_message(

    data: MessageRequest,

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
    # 👤 FIND SENDER
    # =========================

    sender = db.query(User).filter(

        User.email == payload["email"]

    ).first()

    if not sender:

        return {

            "success": False,

            "message": "User not found"

        }

    # =========================
    # 👨‍⚕️ FIND RECEIVER
    # =========================

    receiver = db.query(User).filter(

        User.id == data.receiver_id

    ).first()

    if not receiver:

        return {

            "success": False,

            "message": "Receiver not found"

        }

    # =========================
    # 💬 CREATE MESSAGE
    # =========================

    message = Message(

        sender_id=sender.id,

        receiver_id=data.receiver_id,

        content=data.content

    )

    db.add(message)

    db.commit()

    return {

        "success": True,

        "message": "Message sent"

    }

# =========================
# 📥 GET CONVERSATION
# =========================

@router.get("/messages/{user_id}")

def get_messages(

    user_id: int,

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
    # 👤 CURRENT USER
    # =========================

    current_user = db.query(User).filter(

        User.email == payload["email"]

    ).first()

    if not current_user:

        return {

            "success": False,

            "message": "User not found"

        }

    # =========================
    # 💬 GET MESSAGES
    # =========================

    messages = db.query(Message).filter(

        (
            (Message.sender_id == current_user.id)

            &

            (Message.receiver_id == user_id)

        )

        |

        (
            (Message.sender_id == user_id)

            &

            (Message.receiver_id == current_user.id)

        )

    ).order_by(

        Message.created_at.asc()

    ).all()

    # =========================
    # 📦 FORMAT
    # =========================

    formatted = []

    for msg in messages:

        formatted.append({

            "id": msg.id,

            "sender_id": msg.sender_id,

            "receiver_id": msg.receiver_id,

            "content": msg.content,

            "created_at": str(

                msg.created_at

            )

        })

    return {

        "success": True,

        "messages": formatted

    }