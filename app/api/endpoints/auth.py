from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from jose import jwt
from passlib.context import CryptContext

from app.core.config import SECRET_KEY, ALGORITHM
from app.db.database import get_db
from app.db.models import User

router = APIRouter()

# 🔐 Password hashing (NO bcrypt → works in Termux)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


# =========================
# SIGNUP
# =========================
@router.post("/signup")
def signup(username: str, password: str, db: Session = Depends(get_db)):
    # check if user exists
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # hash password
    hashed_password = pwd_context.hash(password)

    # create user
    user = User(username=username, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created successfully"}


# =========================
# LOGIN
# =========================
@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    # find user
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # verify password
    if not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # 🔥 CREATE TOKEN
    token = jwt.encode(
        {
            "user_id": user.id,
            "username": user.username
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

from jose import jwt, JWTError
from app.core.config import SECRET_KEY, ALGORITHM


def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("user_id")
        username = payload.get("username")

        if user_id is None:
            return None

        return {
            "user_id": user_id,
            "username": username
        }

    except JWTError:
        return None
