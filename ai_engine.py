import time
import json
import re
from openai import OpenAI


# -----------------------------
# STRICT JSON PARSER (UNCHANGED)
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
You are a SENIOR TAX LAWYER working in Big4 (EY/PwC style).

You do NOT classify general information.

You ONLY identify REAL TAX LAW EVENTS:

VALID EVENTS:
- changes in tax law (VAT/CIT/PIT/Excise)
- amendments to acts (Dz.U.)
- binding interpretations / rulings
- draft laws / legislative proposals
- court judgments affecting taxation

INVALID CONTENT (MUST BE IGNORED):
- educational articles ("what is PIT", "how to fill form")
- social programs (Polish Deal explanations, e-TOLL descriptions)
- personal situations ("I earn abroad", "I have freelance income")
- public finance programs (KPO, Polish Fund)
- administrative info (audits, budgeting, IT systems)

Return ONLY JSON.
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
# MAIN PROCESSOR (FIXED LOGIC)
# -----------------------------
def process_batch(news, api_key):

    client = OpenAI(api_key=api_key)

    prompt = f"""
Analyze ONLY REAL TAX LAW EVENTS in Poland.

TASK:
From the list below, extract ONLY items that represent legal or regulatory tax changes.

STRICT RULE:

Return ONLY items that meet ALL conditions:
- legal change OR legislative proposal OR tax ruling
- NOT educational content
- NOT taxpayer guides
- NOT programs or systems explanations

INPUT:
{[
    {"title": n["title"], "source": n["source"]} for n in news
]}

OUTPUT JSON:

{{
  "items": [
    {{
      "title": "clean legal headline (rewrite if needed)",
      "category": "LEAD | STANDARD",
      "score": 0-100,
      "summary": [
        "What EXACTLY changed in tax law",
        "Who is affected (companies / individuals / sector)",
        "Legal basis (Act / Dz.U. / MF / ruling / draft law)"
      ],
      "source": "original source",
      "url": "if available"
    }}
  ]
}}
"""

    result = safe_call(client, prompt)

    items = result.get("items", [])

    # FINAL SAFETY FLOOR
    if len(items) < 2:

        return [
            {
                "title": "Brak istotnych zmian podatkowych w analizowanym okresie",
                "category": "STANDARD",
                "score": 50,
                "summary": [
                    "Nie wykryto zmian legislacyjnych w zakresie VAT/CIT/PIT",
                    "Zidentyfikowane treści mają charakter edukacyjny lub administracyjny",
                    "Brak nowych ustaw lub interpretacji podatkowych"
                ],
                "source": "SYSTEM",
                "url": ""
            }
        ]

    return items
