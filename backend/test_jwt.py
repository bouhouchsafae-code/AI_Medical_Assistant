from auth.jwt_handler import (
    create_access_token,
    verify_token
)

data = {
    "email": "test@gmail.com",
    "role": "doctor"
}

token = create_access_token(data)

print("TOKEN:")
print(token)

print("\nDECODED:")
print(verify_token(token))  