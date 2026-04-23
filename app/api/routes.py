from fastapi import APIRouter

# =========================
# IMPORT ALL ENDPOINTS
# =========================
from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.mcq import router as mcq_router

# =========================
# MAIN ROUTER
# =========================
router = APIRouter()

# =========================
# REGISTER ROUTES
# =========================
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(mcq_router, prefix="/ai", tags=["AI"])
