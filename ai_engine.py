import time
import json
from openai import OpenAI


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
You are a senior TAX POLICY & LEGAL ANALYST for a Big4 firm.

You prepare TAX ALERTS for CFOs.

Rules:
- Write in POLISH
- Be precise and legal
- Do NOT be generic
- Always reference legal context (even if inferred)
- Output ONLY valid JSON
"""
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

    raise Exception(f"OpenAI failed: {last_error}")


def process_batch(news, api_key):

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are preparing a MONTHLY TAX ALERT (Poland).

TASK:
Analyze and score relevance for June 2026 tax developments.

CLASSIFY:

- LEAD TAX NEWS = legislative changes, court rulings, draft laws
- STANDARD TAX NEWS = guidance, interpretations, commentary
- REJECT = irrelevant

IMPORTANT:
- MUST be in POLISH
- MUST include legal context (Dz.U., MF, ISAP if applicable)
- MUST be usable in CFO newsletter

INPUT:
{[
    {
        "title": n["title"],
        "source": n["source"]
    } for n in news
]}

OUTPUT JSON:

{{
  "items": [
    {{
      "title": "...",
      "category": "LEAD | STANDARD | REJECT",
      "score": 0-100,
      "summary": [
        "Co się zmienia (konkret prawny)",
        "Kogo dotyczy (podatnicy / firmy / sektor)",
        "Podstawa prawna lub kontekst (MF / ISAP / ustawa / projekt)"
      ],
      "source": "...",
      "url": "..."
    }}
  ]
}}
"""

    result = safe_call(client, prompt)

    cleaned = []

    for item in result.get("items", []):

        if item["category"] == "REJECT":
            continue

        cleaned.append(item)

    return cleaned
