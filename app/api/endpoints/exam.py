from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import random
import time

from app.db.session import get_db
from app.db.models import MCQ, ExamHistory
from app.core.security import verify_token

router = APIRouter()

EXAM_SESSIONS = {}

@router.get("/start")
def start_exam(
    topic: str,
    limit: int = 5,
    duration: int = 300,
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):

    all_mcqs = db.query(MCQ).filter(MCQ.topic == topic).all()

    selected = random.sample(all_mcqs, min(len(all_mcqs), limit))

    exam_id = str(int(time.time()))

    EXAM_SESSIONS[exam_id] = {
        "topic": topic,
        "start_time": int(time.time()),
        "duration": duration,
        "questions": {q.id: q.answer for q in selected},
        "user_id": user.get("user_id")
    }

    return {
        "exam_id": exam_id,
        "questions": [
            {
                "id": q.id,
                "question": q.question,
                "options": ["A", "B", "C", "D"]
            }
            for q in selected
        ]
    }


@router.post("/submit")
def submit_exam(exam_id: str, answers: dict,
                user=Depends(verify_token),
                db: Session = Depends(get_db)):

    session = EXAM_SESSIONS[exam_id]

    score = 0
    total = len(session["questions"])

    for q_id, correct in session["questions"].items():
        if answers.get(str(q_id)) == correct:
            score += 1

    history = ExamHistory(
        user_id=session["user_id"],
        topic=session["topic"],
        score=score,
        total=total
    )

    db.add(history)
    db.commit()

    return {
        "score": score,
        "total": total,
        "percentage": round((score / total) * 100, 2)
    }
