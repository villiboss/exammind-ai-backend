from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import ExamHistory

router = APIRouter()


@router.get("/top")
def leaderboard(db: Session = Depends(get_db)):

    records = db.query(ExamHistory).all()

    users = {}

    for r in records:
        if r.user_id not in users:
            users[r.user_id] = {"score": 0, "total": 0}

        users[r.user_id]["score"] += r.score
        users[r.user_id]["total"] += r.total

    result = []

    for uid, v in users.items():
        accuracy = (v["score"] / v["total"]) * 100
        result.append({
            "user_id": uid,
            "accuracy": round(accuracy, 2)
        })

    return sorted(result, key=lambda x: x["accuracy"], reverse=True)
