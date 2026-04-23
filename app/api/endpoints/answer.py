
from fastapi import APIRouter

router = APIRouter()

# -------------------------
# AI ANSWER ANALYZER
# -------------------------
def analyze_answer(answer: str, topic: str):

    word_count = len(answer.split())

    # basic scoring logic (free AI simulation)
    score = 0

    if word_count > 50:
        score += 3
    elif word_count > 20:
        score += 2
    else:
        score += 1

    if "because" in answer.lower() or "therefore" in answer.lower():
        score += 2

    if topic.lower() in answer.lower():
        score += 2

    if len(answer) > 200:
        score += 3

    score = min(score, 10)

    # feedback system
    feedback = []

    if word_count < 50:
        feedback.append("Expand your answer with more points and examples.")

    if "because" not in answer.lower():
        feedback.append("Add reasoning words like 'because', 'therefore'.")

    if topic.lower() not in answer.lower():
        feedback.append(f"Include direct reference to {topic} in your answer.")

    if word_count > 150:
        feedback.append("Good length — ensure clarity and structure.")

    return {
        "score": score,
        "word_count": word_count,
        "feedback": feedback,
        "suggestion": "Use introduction → body → conclusion structure for UPSC answers."
    }


# -------------------------
# API ENDPOINT
# -------------------------
@router.get("/analyze")
def analyze(topic: str, answer: str):

    result = analyze_answer(answer, topic)

    return {
        "topic": topic,
        "analysis": result
    }
