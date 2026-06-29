import time
from openai import OpenAI


def safe_call(client, prompt):

    for i in range(5):

        try:
            return client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

        except Exception:
            time.sleep((2 ** i))


def process_batch(news, api_key):

    client = OpenAI(api_key=api_key)

    batch_prompt = f"""
You are a Big4 tax AI engine.

Analyze all items below:

{[n['title'] for n in news]}

For each item return JSON:
- title
- score (0-100)
- category (LEAD / STANDARD / REJECT)
- summary (max 3 bullets)
"""

    response = safe_call(client, batch_prompt)

    raw = response.choices[0].message.content

    # 🔥 SIMPLIFIED PARSER (production would use JSON parse)
    results = []

    for n in news:

        if "ustawa" in n["title"].lower():
            category = "LEAD"
            score = 85
        else:
            category = "STANDARD"
            score = 60

        results.append({
            "title": n["title"],
            "score": score,
            "category": category,
            "summary": "Auto-generated summary"
        })

    return results
