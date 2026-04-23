from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import router AFTER app creation
from app.api.routes import router

app = FastAPI(title="ExamMind AI Backend")

# ✅ CORS FIX (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later you can restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ include all routes
app.include_router(router)


# optional root test route
@app.get("/")
def home():
    return {"message": "Backend is running 🚀"}
