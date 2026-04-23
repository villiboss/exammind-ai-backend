
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import random

from app.db.session import get_db
from app.db.models import MCQ
from app.api.endpoints.auth_jwt import verify_token

router = APIRouter()


# -------------------------
# ADAPTIVE LOGIC
# -------------------------
def get_level(score: int):
    if score < 3:
        return "easy"
    elif score < 7:
        return "medium"
    else:
        return "hard"


# -------------------------
# ADAPTIVE QUESTIONS
# -------------------------
@router.post("/generate")
def adaptive_questions(
    topic: str = "physics",
    score: int = 0,
    db: Session = Depends(get_db),
    user=Depends(verify_token)
):

    level = get_level(score)

    # filter by topic (basic for now)
    questions = db.query(MCQ).filter(MCQ.topic == topic).all()

    random.shuffle(questions)

    selected = questions[:5]

    return {
        "topic": topic,
        "user_score": score,
        "difficulty": level,
        "questions": [
            {
                "id": q.id,
                "question": q.question,
                "options": ["A", "B", "C", "D"]
            }
            for q in selected
        ]
    }
