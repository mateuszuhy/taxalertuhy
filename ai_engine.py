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

        raise ValueError("Invalid JSON output")


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
Jesteś analitykiem podatkowym (Big4).

ZASADY:
- język WYŁĄCZNIE polski
- NIE zmieniasz struktury danych
- NIE tworzysz nowych pól
- NIE usuwasz pól
- NIE oceniasz newsów
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
Przekształć dane wejściowe do ujednoliconego formatu podatkowego.

DANE:
{news}

ZWRÓĆ WYŁĄCZNIE JSON:

{{
  "items": [
    {{
      "title": "tytuł po polsku",
      "what_changed": "opis zmiany (PL)",
      "impact": "wpływ podatkowy (PL, CFO style)",
      "legal_basis": "podstawa prawna (PL)",
      "source": "źródło",
      "url": "link"
    }}
  ]
}}

ZASADY:
- NIE używaj angielskiego
- NIE skracaj do bulletów
- NIE zmieniaj struktury JSON
"""

    result = safe_call(client, prompt)

    return result.get("items", [])
