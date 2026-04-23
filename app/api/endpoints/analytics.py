from fastapi import APIRouter

router = APIRouter()

# -------------------------
# RANK PREDICTION ENGINE
# -------------------------
def predict_rank(score: float, total: int, difficulty: str = "medium"):

    accuracy = (score / total) * 100 if total > 0 else 0

    # base percentile logic
    if accuracy >= 90:
        percentile = 99
        rank_range = "Top 1% (1 - 10,000)"
    elif accuracy >= 75:
        percentile = 95
        rank_range = "Top 5% (10,000 - 50,000)"
    elif accuracy >= 60:
        percentile = 85
        rank_range = "Top 15% (50,000 - 150,000)"
    elif accuracy >= 40:
        percentile = 60
        rank_range = "Average (150,000 - 300,000)"
    else:
        percentile = 30
        rank_range = "Below Average (300,000+)"

    # difficulty adjustment
    if difficulty == "hard":
        percentile = min(100, percentile + 2)

    return {
        "accuracy": round(accuracy, 2),
        "percentile": percentile,
        "estimated_rank_range": rank_range,
        "performance_level": (
            "Excellent" if accuracy >= 85 else
            "Good" if accuracy >= 70 else
            "Average" if accuracy >= 50 else
            "Needs Improvement"
        ),
        "advice": generate_advice(accuracy)
    }


# -------------------------
# AI ADVICE SYSTEM
# -------------------------
def generate_advice(accuracy):

    if accuracy >= 85:
        return "Keep practicing advanced questions and timed mock tests."
    elif accuracy >= 60:
        return "Focus on weak topics and revise regularly."
    else:
        return "Strengthen basics and practice daily MCQs."


# -------------------------
# API ENDPOINT
# -------------------------
@router.get("/predict")
def get_prediction(score: int, total: int, difficulty: str = "medium"):

    result = predict_rank(score, total, difficulty)

    return {
        "message": "Rank prediction generated",
        "score": score,
        "total": total,
        "result": result
    }
