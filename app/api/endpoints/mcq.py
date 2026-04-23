from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import MCQ

router = APIRouter()


@router.get("/mcq")
def get_mcqs(db: Session = Depends(get_db)):
    return db.query(MCQ).all()
