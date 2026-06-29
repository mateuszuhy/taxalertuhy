import time
import json
import re
from openai import OpenAI


# -----------------------------
# SAFE JSON PARSER
# -----------------------------
def extract_json(text: str):

    if not text:
        raise ValueError("Empty response")

    text = text.strip()

    text = re.sub(r"^```json", "", text)
    text = re.sub(r"^```", "", text)
    text = re.sub(r"```$", "", text)

    text = text.strip()

    try:
        return json.loads(text)
    except:

        match = re.search(r"\{.*\}", text, re.DOTALL)

        if match:
            return json.loads(match.group())

        raise ValueError(f"Invalid JSON: {text[:300]}")


# -----------------------------
# SAFE CALL
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
                        "content": """
You are a Big4 TAX INTELLIGENCE ANALYST.

Rules:
- Always respond in POLISH
- Never output anything outside JSON
- Prefer completeness over strict filtering
- Always assign relevance score (0-100)
"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            content = response.choices[0].message.content

            return extract_json(content)

        except Exception as e:
            last_error = e
            time.sleep(2 ** i)

    raise Exception(f"OpenAI failed: {last_error}")


# -----------------------------
# MAIN ENGINE
# -----------------------------
def process_batch(news, api_key):

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are building a MONTHLY TAX ALERT (Poland, CFO level).

TASK:
Analyze tax-related news and assign relevance.

IMPORTANT RULES:
- DO NOT over-filter
- Every item must get a score (0–100)
- Even weak tax relevance must be classified
- No REJECT category anymore

CLASSIFICATION:
- LEAD = legal changes, rulings, amendments
- STANDARD = interpretations, guidance, commentary
- LOW = weak but still tax-related context

INPUT:
{[
    {"title": n["title"], "source": n["source"]} for n in news
]}

OUTPUT JSON:

{{
  "items": [
    {{
      "title": "...",
      "category": "LEAD | STANDARD | LOW",
      "score": 0-100,
      "summary": [
        "Co się zmienia (konkret podatkowy)",
        "Wpływ na podatników / firmy",
        "Kontekst prawny (MF / ISAP / ustawa / interpretacja)"
      ],
      "source": "...",
      "url": "..."
    }}
  ]
}}
"""

    result = safe_call(client, prompt)

    items = result.get("items", [])

    # fallback guard (VERY IMPORTANT)
    if len(items) < 3:

        return [
            {
                "title": "Brak danych – fallback system",
                "category": "LOW",
                "score": 10,
                "summary": [
                    "System nie znalazł wystarczającej liczby danych",
                    "Możliwy problem z feedem źródeł",
                    "Zalecana weryfikacja scraperów"
                ],
                "source": "SYSTEM",
                "url": ""
            }
        ]

    return items
