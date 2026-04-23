import os

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# =========================
# AI CONFIG
# =========================
AI_PROVIDER = os.getenv("AI_PROVIDER", "mock")  # mock | openai
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
