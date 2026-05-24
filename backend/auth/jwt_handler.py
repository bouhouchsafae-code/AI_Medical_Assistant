from jose import jwt, JWTError
from datetime import datetime, timedelta

# =========================
# 🔐 JWT CONFIG
# =========================

SECRET_KEY = "SUPER_SECRET_AI_MEDICAL_KEY"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60

# =========================
# 🔑 Create access token
# =========================

def create_access_token(data: dict):

    # copy payload
    to_encode = data.copy()

    # expiration
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # add expiration
    to_encode.update({
        "exp": expire
    })

    # encode token
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

# =========================
# ✅ Verify token
# =========================

def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        print("\n✅ TOKEN PAYLOAD:")
        print(payload)

        return payload

    except JWTError as e:

        print("\n❌ JWT ERROR:")
        print(e)

        return None

    except Exception as e:

        print("\n❌ GENERAL ERROR:")
        print(e)

        return None