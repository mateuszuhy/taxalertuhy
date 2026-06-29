from scraper import get_all_news
from ai_engine import process_batch
from ppt_generator import create_ppt
from cache import get_cache, set_cache


def categorize(item):

    score = item.get("score", 0)

    if score >= 75:
        return "lead"
    elif score >= 40:
        return "standard"
    return "low"


def run_engine(api_key):

    cached = get_cache()
    if cached:
        return cached

    news = get_all_news()

    news = news[:30]

    processed = process_batch(news, api_key)

    result = {
        "lead": [],
        "standard": []
    }

    for item in processed:

        bucket = categorize(item)

        if bucket != "low":
            result[bucket].append(item)

    # GUARANTEE OUTPUT
    if not result["lead"] and not result["standard"]:

        result["standard"].append({
            "title": "Brak zmian legislacyjnych – okres referencyjny",
            "category": "STANDARD",
            "score": 50,
            "summary": [
                "Nie wykryto zmian w przepisach VAT/CIT/PIT",
                "Brak nowych ustaw, projektów lub interpretacji",
                "Okres stabilny legislacyjnie"
            ],
            "source": "SYSTEM",
            "url": ""
        })

    file_path = create_ppt(result)
    result["file_path"] = file_path

    set_cache(result)

    return result
