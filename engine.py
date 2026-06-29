from scraper import get_news
from openai import OpenAI
from ppt_generator import create_ppt

def run_tax_engine(api_key):

    client = OpenAI(api_key=api_key)

    news = get_news()

    processed = []

    for n in news:

        prompt = f"""
You are a Big4 tax AI.

Classify and summarize:

TEXT:
{n['title']}

Return:
- category: LEAD/STANDARD/REJECT
- score (0-100)
- summary (max 5 bullets)
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        processed.append(response.choices[0].message.content)

    result = {
        "lead": [p for p in processed if "LEAD" in p],
        "standard": [p for p in processed if "STANDARD" in p]
    }

    create_ppt(result)

    return result
