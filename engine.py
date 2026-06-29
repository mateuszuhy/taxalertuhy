from scraper import get_all_news
from ai_engine import process_batch
from ppt_generator import create_ppt
from cache import get_cache, set_cache


def run_engine(api_key):

    cached = get_cache()

    if cached:
        return cached

    news = get_all_news()

    # 🔥 safety limit (Streamlit stability)
    news = news[:6]

    processed = process_batch(news, api_key)

    result = {
        "lead": [n for n in processed if n["category"] == "LEAD"],
        "standard": [n for n in processed if n["category"] == "STANDARD"]
    }

    file_path = create_ppt(result)

    result["file_path"] = file_path  # 🔥 IMPORTANT FIX

    set_cache(result)

    return result
