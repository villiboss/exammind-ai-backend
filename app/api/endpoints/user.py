from fastapi import APIRouter, Header, HTTPException
from app.services.auth_service import get_current_user

router = APIRouter()

@router.get("/me")
def get_me(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid format")

    token = authorization.replace("Bearer ", "")
    user = get_current_user(token)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {
        "user_id": user["user_id"],
        "username": user["username"]
    }
