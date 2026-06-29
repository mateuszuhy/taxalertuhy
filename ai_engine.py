import time
import json
from openai import OpenAI


# -----------------------------
# SAFE CALL (HARD GUARANTEE)
# -----------------------------
def safe_call(client, prompt):

    last_error = None

    for i in range(5):

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a tax classification engine. Always return valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0
            )

            content = response.choices[0].message.content

            # 🔥 FORCE JSON PARSE
            return json.loads(content)

        except Exception as e:
            last_error = e
            time.sleep(2 ** i)

    raise Exception(f"OpenAI failed after retries: {last_error}")


# -----------------------------
# MAIN BATCH PROCESSOR
# -----------------------------
def process_batch(news, api_key):

    client = OpenAI(api_key=api_key)

    prompt = f"""
Classify ALL items below into structured JSON.

RULES:
- return ONLY valid JSON
- no commentary
- no markdown

OUTPUT FORMAT:
{{
  "items": [
    {{
      "title": "...",
      "category": "LEAD | STANDARD | REJECT",
      "score": 0-100,
      "summary": ["bullet1", "bullet2", "bullet3"]
    }}
  ]
}}

INPUT:
{[n['title'] for n in news]}
"""

    result = safe_call(client, prompt)

    cleaned = []

    for item in result.get("items", []):

        if item["category"] == "REJECT":
            continue

        cleaned.append({
            "title": item["title"],
            "category": item["category"],
            "score": item["score"],
            "summary": item["summary"]
        })

    return cleaned
