from fastapi import APIRouter

router = APIRouter()

@router.get("/generate")
def generate_notes(topic: str = "general"):
    return {
        "topic": topic,
        "notes": f"Generated notes for {topic}",
        "level": "basic"
    }
