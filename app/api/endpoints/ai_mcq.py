from fastapi import APIRouter, Header, HTTPException
from app.services.auth_service import get_current_user
from app.services.ai_service import SmartAI

router = APIRouter()


@router.post("/mcq")
def generate_mcq(topic: str, authorization: str = Header(None)):

    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.replace("Bearer ", "")

    user = get_current_user(token)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    data = SmartAI.mcq(topic)

    return {
        "topic": topic,
        "questions": data.get("questions", []),
        "user": user["username"]
    }
