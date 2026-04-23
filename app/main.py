from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ======================
# CREATE APP FIRST
# ======================
app = FastAPI(title="ExamMind AI Backend")

# ======================
# CORS MIDDLEWARE
# ======================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
        "https://exammind-ai-backend.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================
# ROUTES IMPORT
# ======================
from app.api.routes import router

app.include_router(router)


# ======================
# TEST ROUTE
# ======================
@app.get("/")
def home():
    return {"message": "Backend running 🚀"}
