from fastapi import APIRouter
import random

router = APIRouter()

@router.get("/mcq")
def generate_mcq(topic: str):
    questions = [
        {
            "question": f"What is the basic concept of {topic}?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "Option A"
        },
        {
            "question": f"Which is related to {topic}?",
            "options": ["X", "Y", "Z", "W"],
            "answer": "Y"
        }
    ]

    return {
        "topic": topic,
        "questions": questions
    }
