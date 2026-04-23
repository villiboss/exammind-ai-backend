from fastapi import APIRouter, Header, HTTPException
from app.services.auth_service import get_current_user
from app.services.ai_service import SmartAI

router = APIRouter()


@router.post("/explain")
def explain(question: str, authorization: str = Header(None)):

    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.replace("Bearer ", "")

    user = get_current_user(token)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    answer = SmartAI.explain(question)

    return {
        "question": question,
        "answer": answer,
        "user": user["username"]
    }
