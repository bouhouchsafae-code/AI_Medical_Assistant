from fastapi.security import OAuth2PasswordBearer
from auth.jwt_handler import verify_token

# =========================
# 🔐 OAuth2 scheme
# =========================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)

# =========================
# 👤 Current user
# =========================

def get_current_user(
    token: str
):

    print("\nTOKEN:", token)

    payload = verify_token(token)

    print("PAYLOAD:", payload)

    return payload