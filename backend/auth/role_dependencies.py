from fastapi import Depends, HTTPException, status

from auth.auth_routes import (
    oauth2_scheme
)

from auth.jwt_handler import (
    verify_token
)

# =========================
# 🔐 Role checker
# =========================

def role_required(required_role: str):

    def role_checker(

        token: str = Depends(oauth2_scheme)

    ):

        # verify token
        payload = verify_token(token)

        # invalid token
        if payload is None:

            raise HTTPException(

                status_code=status.HTTP_401_UNAUTHORIZED,

                detail="Unauthorized"

            )

        # wrong role
        if payload["role"] != required_role:

            raise HTTPException(

                status_code=status.HTTP_403_FORBIDDEN,

                detail="Access denied"

            )

        return payload

    return role_checker     