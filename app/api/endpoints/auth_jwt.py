from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from jose import jwt, JWTError
import time

from app.db.session import get_db
from app.db.models import User

router = APIRouter()

# -------------------------
# JWT CONFIG
# -------------------------
SECRET_KEY = "exam_mind_secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 86400  # 1 day


# -------------------------
# CREATE TOKEN
# -------------------------
def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = int(time.time()) + ACCESS_TOKEN_EXPIRE_SECONDS
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# -------------------------
# REGISTER USER (SAFE)
# -------------------------
@router.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):

    user = User(username=username, password=password)
    db.add(user)

    try:
        db.commit()
        db.refresh(user)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    return {
        "message": "User registered successfully",
        "user_id": user.id
    }


# -------------------------
# LOGIN USER (TOKEN RETURN)
# -------------------------
@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(
        User.username == username,
        User.password == password
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({
        "user_id": user.id,
        "username": user.username
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# -------------------------
# VERIFY TOKEN (USED IN APIs)
# -------------------------
def verify_token(authorization: str = Header(None)):

    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
