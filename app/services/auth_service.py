from jose import jwt, JWTError
from app.core.config import SECRET_KEY, ALGORITHM


def create_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


def get_current_user(token: str):
    payload = decode_token(token)

    if not payload:
        return None

    return {
        "user_id": payload.get("user_id"),
        "username": payload.get("username")
    }
