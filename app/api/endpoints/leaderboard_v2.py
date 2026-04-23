from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Leaderboard, User
from app.services.auth_service import get_current_user

router = APIRouter()


# =========================
# SAVE SCORE (AUTH REQUIRED)
# =========================
@router.post("/save-score")
def save_score(
    score: int,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    print("HEADER:", authorization)

    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = authorization.replace("Bearer ", "")

    print("TOKEN:", token)

    user_data = get_current_user(token)

    print("DECODED:", user_data)

    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == user_data["user_id"]).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_score = Leaderboard(user_id=user.id, score=score)
    db.add(new_score)
    db.commit()

    return {
        "message": "Score saved successfully",
        "username": user.username,
        "score": score
    }


# =========================
# GET LEADERBOARD (RANKED)
# =========================
@router.get("/")
def get_leaderboard(db: Session = Depends(get_db)):
    results = (
        db.query(User.username, Leaderboard.score)
        .join(Leaderboard, User.id == Leaderboard.user_id)
        .order_by(Leaderboard.score.desc())
        .all()
    )

    leaderboard = []
    rank = 1

    for row in results:
        leaderboard.append({
            "rank": rank,
            "username": row.username,
            "score": row.score
        })
        rank += 1

    return {"leaderboard": leaderboard}
