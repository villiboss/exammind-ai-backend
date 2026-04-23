from fastapi import APIRouter

router = APIRouter()

from app.api.endpoints import auth
from app.api.endpoints import leaderboard_v2
from app.api.endpoints import ai_explain
from app.api.endpoints import ai_mcq


router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(leaderboard_v2.router, prefix="/leaderboard", tags=["Leaderboard"])
router.include_router(ai_explain.router, prefix="/ai", tags=["AI"])
router.include_router(ai_mcq.router, prefix="/ai", tags=["AI"])


@router.get("/health")
def health():
    return {"status": "ok"}
