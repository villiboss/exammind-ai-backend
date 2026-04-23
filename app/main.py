from fastapi import FastAPI
from app.api.routes import router
from app.db.database import Base, engine

app = FastAPI()

# safe DB init
Base.metadata.create_all(bind=engine)

app.include_router(router)


@app.get("/")
def home():
    return {"status": "ExamMind AI running"}
