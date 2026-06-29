import time
import json
import re
from openai import OpenAI


def extract_json(text):

    text = text.strip()

    text = re.sub(r"^```json", "", text)
    text = re.sub(r"^```", "", text)
    text = re.sub(r"```$", "", text)

    try:
        return json.loads(text)
    except:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())

        raise ValueError("Invalid JSON")


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
Jesteś analitykiem prawa podatkowego (Big4).

ZASADY:
- język WYŁĄCZNIE polski
- NIE tworzysz narracji
- NIE oceniasz znaczenia
- NIE odrzucasz newsów
- tylko ekstrakcja faktów
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
Przekształć poniższe dane w strukturalne fakty podatkowe.

DANE:
{news}

ZWRÓĆ JSON:

{{
  "items": [
    {{
      "title": "tytuł po polsku",
      "what_changed": "opis zmiany podatkowej (PL)",
      "impact": "wpływ dla podatników (PL, CFO style)",
      "legal_basis": "podstawa prawna (PL)",
      "source": "źródło",
      "url": "link"
    }}
  ]
}}
"""

    result = safe_call(client, prompt)

    return result.get("items", [])
