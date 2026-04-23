from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import ExamHistory

router = APIRouter()


@router.get("/stats")
def stats(user_id: int, db: Session = Depends(get_db)):

    records = db.query(ExamHistory).filter(
        ExamHistory.user_id == user_id
    ).all()

    total = sum(r.total for r in records)
    score = sum(r.score for r in records)

    accuracy = (score / total) * 100 if total else 0

    return {
        "exams_taken": len(records),
        "accuracy": round(accuracy, 2)
    }
