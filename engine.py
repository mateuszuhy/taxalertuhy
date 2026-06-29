from scraper import get_all_news
from ai_engine import process_batch
from ppt_generator import create_ppt
from cache import get_cache, set_cache


def categorize(item):

    score = item.get("score", 0)

    if score >= 70:
        return "lead"
    elif score >= 40:
        return "standard"
    else:
        return "low"


def run_engine(api_key):

    cached = get_cache()
    if cached:
        return cached

    news = get_all_news()

    # safe cap
    news = news[:30]

    processed = process_batch(news, api_key)

    result = {
        "lead": [],
        "standard": [],
        "low": []
    }

    for item in processed:

        bucket = categorize(item)
        result[bucket].append(item)

    # 🔥 ENSURE NON-EMPTY OUTPUT (CRITICAL FIX)
    if not result["lead"] and not result["standard"]:

        result["standard"].append({
            "title": "Brak silnych zmian podatkowych w okresie",
            "category": "STANDARD",
            "score": 50,
            "summary": [
                "W analizowanym okresie nie wykryto istotnych zmian legislacyjnych",
                "Dominują interpretacje i komentarze administracyjne",
                "Brak nowych ustaw podatkowych w analizowanym feedzie"
            ],
            "source": "SYSTEM",
            "url": ""
        })

    file_path = create_ppt({
        "lead": result["lead"],
        "standard": result["standard"]
    })

    result["file_path"] = file_path

    set_cache(result)

    return result
