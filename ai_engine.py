import time
import json
import re
from openai import OpenAI


# -----------------------------
# JSON EXTRACTION (ROBUST)
# -----------------------------
def extract_json(text: str):

    if not text:
        raise ValueError("Empty response from OpenAI")

    text = text.strip()

    # remove markdown fences
    text = re.sub(r"^```json", "", text)
    text = re.sub(r"^```", "", text)
    text = re.sub(r"```$", "", text)

    text = text.strip()

    # try direct JSON parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # fallback: extract JSON block
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    # last resort debug output
    raise ValueError(f"Invalid JSON from model (first 300 chars): {text[:300]}")


# -----------------------------
# SAFE OPENAI CALL
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
                        "content": (
                            "You are a senior TAX LAW analyst for a Big4 firm. "
                            "Return ONLY valid JSON. No markdown. No commentary. No text outside JSON."
                        )
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

    raise Exception(f"OpenAI failed after retries: {last_error}")


# -----------------------------
# MAIN PROCESSOR
# -----------------------------
def process_batch(news, api_key):

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are preparing a MONTHLY TAX ALERT for Poland (CFO audience).

TASK:
Analyze tax-related legislative and regulatory developments.

STRICT RULES:
- Output ONLY JSON
- No markdown
- No commentary
- No extra text
- MUST be in Polish
- Focus only on VAT, CIT, PIT, tax procedures, tax law changes

CLASSIFICATION:
- LEAD = legislative changes / court rulings / binding interpretations
- STANDARD = guidance / commentary / explanations
- REJECT = irrelevant content

INPUT NEWS:
{[
    {
        "title": n["title"],
        "source": n.get("source", "")
    } for n in news
]}

OUTPUT FORMAT:

{{
  "items": [
    {{
      "title": "string",
      "category": "LEAD | STANDARD | REJECT",
      "score": 0,
      "summary": [
        "Opis zmiany podatkowej (konkretnie)",
        "Kogo dotyczy (firmy / osoby fizyczne / sektor)",
        "Podstawa prawna lub kontekst (Dz.U., MF, ISAP, projekt ustawy)"
      ],
      "source": "string (optional)",
      "url": "string (optional)"
    }}
  ]
}}
"""

    result = safe_call(client, prompt)

    items = result.get("items", [])

    cleaned = []

    for item in items:

        if item.get("category") == "REJECT":
            continue

        cleaned.append(item)

    return cleaned
