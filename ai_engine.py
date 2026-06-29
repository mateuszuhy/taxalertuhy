import time
import json
from openai import OpenAI


# -----------------------------
# SAFE CALL (ROBUST)
# -----------------------------
def safe_call(client, prompt):

    last_error = None

    for i in range(5):

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a senior TAX LAW analyst. Return ONLY valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            content = response.choices[0].message.content

            return json.loads(content)

        except Exception as e:
            last_error = e
            time.sleep(2 ** i)

    raise Exception(f"OpenAI failed after retries: {last_error}")


# -----------------------------
# BATCH PROCESSOR (TAX ONLY)
# -----------------------------
def process_batch(news, api_key):

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are a Big4 TAX POLICY AI engine.

TASK:
Analyze ONLY tax legislation and regulatory changes.

STRICT FILTER:
- Ignore administrative, HR, budgeting, internal audit content
- Only VAT, CIT, PIT, tax law, procedures, ordinances

INPUT ITEMS:
{[n['title'] for n in news]}

OUTPUT JSON FORMAT:

{{
  "items": [
    {{
      "title": "...",
      "category": "LEAD | STANDARD | REJECT",
      "score": 0-100,
      "summary": [
        "Describe exact legal tax change",
        "Explain who is affected (companies / individuals)",
        "State timing or legal status (draft / adopted / effective)"
      ]
    }}
  ]
}}
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
