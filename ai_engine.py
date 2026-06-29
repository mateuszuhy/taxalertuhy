import time
import json
import re
from openai import OpenAI


def extract_json(text):

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
You are a BIG4 TAX LEGAL ANALYST.

You do NOT generate news.
You ONLY analyze provided legal tax sources.

Rules:
- Only Polish
- No hallucinations
- Always cite source
- Focus on legal changes only
"""
                    },
                    {"role": "user", "content": prompt}
                ]
            )

            return extract_json(response.choices[0].message.content)

        except Exception as e:
            last_error = e
            time.sleep(2 ** i)

    raise Exception(f"OpenAI failed: {last_error}")


def process_batch(news, api_key):

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are preparing a MONTHLY TAX ALERT (Poland, CFO level).

ONLY analyze REAL TAX LAW EVENTS.

INPUT SOURCES (already scraped, do not invent new ones):
{[
    {
        "title": n["title"],
        "source": n["source"],
        "url": n.get("url", "")
    } for n in news
]}

TASK:
Select ONLY items that are:
- legal changes (VAT/CIT/PIT/Excise)
- draft laws (RCL)
- interpretations (MF)
- rulings affecting taxation

EXCLUDE:
- educational content
- guides
- programs (KPO, Polish Deal explanations)
- administrative systems (e-TOLL etc.)

OUTPUT JSON:

{{
  "items": [
    {{
      "title": "clean legal headline",
      "category": "LEAD | STANDARD",
      "score": 0-100,

      "summary": [
        "WHAT changed in law (precise)",
        "WHO is affected (business / individuals / sector)",
        "LEGAL BASIS (Dz.U., MF, ISAP, RCL, ruling)"
      ],

      "source": "original source",
      "url": "original URL or null"
    }}
  ]
}}
"""

    result = safe_call(client, prompt)

    items = result.get("items", [])

    # fallback safety
    if len(items) < 2:
        return [
            {
                "title": "Brak istotnych zmian podatkowych w okresie",
                "category": "STANDARD",
                "score": 50,
                "summary": [
                    "Nie zidentyfikowano zmian legislacyjnych VAT/CIT/PIT",
                    "Dostępne treści mają charakter informacyjny lub administracyjny",
                    "Brak nowych aktów prawnych w analizowanym okresie"
                ],
                "source": "SYSTEM",
                "url": ""
            }
        ]

    return items
