from app.core.config import AI_PROVIDER, OPENAI_API_KEY


class SmartAI:

    # =========================
    # EXPLAIN AI
    # =========================
    @staticmethod
    def explain(question: str):

        if AI_PROVIDER == "mock" or not OPENAI_API_KEY:
            return f"[MOCK AI]\nExplanation: {question}\n(Simple answer)"

        try:
            from openai import OpenAI

            client = OpenAI(api_key=OPENAI_API_KEY)

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a teacher."},
                    {"role": "user", "content": question}
                ]
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"AI ERROR: {str(e)}"


    # =========================
    # MCQ AI
    # =========================
    @staticmethod
    def mcq(topic: str):

        if AI_PROVIDER == "mock" or not OPENAI_API_KEY:
            return {
                "questions": [
                    {
                        "question": f"What is {topic}?",
                        "options": ["A", "B", "C", "D"],
                        "answer": "A"
                    }
                ]
            }

        try:
            from openai import OpenAI
            import json

            client = OpenAI(api_key=OPENAI_API_KEY)

            prompt = f"""
Create 3 MCQs on {topic}.
Return ONLY JSON:
{{
  "questions": [
    {{
      "question": "...",
      "options": ["A","B","C","D"],
      "answer": "A"
    }}
  ]
}}
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are MCQ generator."},
                    {"role": "user", "content": prompt}
                ]
            )

            return json.loads(response.choices[0].message.content)

        except Exception:
            return {
                "questions": [
                    {
                        "question": f"Basic question on {topic}",
                        "options": ["A", "B", "C", "D"],
                        "answer": "A"
                    }
                ]
            }
