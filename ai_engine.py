import time
import json
import re
from openai import OpenAI


def extract_json(text):

    if not text:
        raise ValueError("Empty response")

    text = re.sub(r"^```json", "", text.strip())
    text = re.sub(r"^```", "", text)
    text = re.sub(r"```$", "", text)

    try:
        return json.loads(text)
    except:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())

        raise ValueError(text[:300])


def safe_call(client, prompt):

    for i in range(5):

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0,
                messages=[
                    {
                        "role": "system",
                        "content": """
You are a TAX FACT ANALYST.

You ONLY extract facts from provided legal tax news.

You do NOT decide relevance.

You do NOT filter news.

You do NOT remove anything.

Return ONLY JSON.
"""
                    },
                    {"role": "user", "content": prompt}
                ]
            )

            return extract_json(response.choices[0].message.content)

        except Exception:
            time.sleep(2 ** i)

    raise Exception("AI failed")


def process_batch(news, api_key):

    client = OpenAI(api_key=api_key)

    prompt = f"""
Extract tax facts from the following news items.

DO NOT FILTER ANYTHING.

INPUT:
{news}

OUTPUT JSON:

{{
  "items": [
    {{
      "title": "clean headline",
      "category": "LEAD | STANDARD",
      "impact_score": 0-100,
      "summary": {{
        "what_changed": "...",
        "impact": "...",
        "legal_basis": "..."
      }},
      "source": "...",
      "url": "..."
    }}
  ]
}}
"""

    result = safe_call(client, prompt)

    return result.get("items", [])
