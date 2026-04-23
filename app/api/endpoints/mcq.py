kfrom fastapi import APIRouter

router = APIRouter()

# =========================
# SAMPLE MCQ DATABASE (TEMP)
# =========================
QUESTIONS_DB = {
    "physics": [
        {
            "question": "What is Newton's First Law?",
            "options": [
                "Law of inertia",
                "F = ma",
                "E = mc2",
                "Gravity law"
            ],
            "answer": "Law of inertia"
        },
        {
            "question": "Unit of Force?",
            "options": ["Newton", "Joule", "Watt", "Pascal"],
            "answer": "Newton"
        }
    ]
}

# =========================
# GET QUESTIONS
# =========================
@router.get("/mcq")
def get_mcq(topic: str):
    return {
        "topic": topic,
        "questions": QUESTIONS_DB.get(topic.lower(), [])
    }

# =========================
# CHECK ANSWERS
# =========================
@router.post("/submit")
def submit_answers(payload: dict):
    questions = payload.get("questions", [])
    answers = payload.get("answers", [])

    score = 0

    for q, a in zip(questions, answers):
        if q["answer"] == a:
            score += 1

    return {
        "total": len(questions),
        "score": score
    }
