from scraper import get_all_news
from ai_engine import process_batch
from ppt_generator import create_ppt
from cache import get_cache, set_cache


def run_engine(api_key):

    cached = get_cache()

    if cached:
        return cached

    news = get_all_news()

    # 🔥 HARD LIMIT (stability)
    news = news[:6]

    processed = process_batch(news, api_key)

    result = {
        "lead": [n for n in processed if n["category"] == "LEAD"],
        "standard": [n for n in processed if n["category"] == "STANDARD"]
    }

    create_ppt(result)

    set_cache(result)

    return result
