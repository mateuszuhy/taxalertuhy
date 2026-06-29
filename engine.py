from scraper import get_all_news
from ai_engine import process_batch
from editor import format_newsletter
from ppt_generator import create_ppt
from cache import get_cache, set_cache


def run_engine(api_key):

    cached = get_cache()
    if cached:
        return cached

    news = get_all_news()

    news = news[:40]

    items = process_batch(news, api_key)

    # fallback safety
    if not items:
        items = [{
            "title": "Brak istotnych zmian podatkowych",
            "what_changed": "Nie zidentyfikowano zmian legislacyjnych",
            "impact": "Stabilne otoczenie podatkowe",
            "legal_basis": "Brak nowych aktów prawnych",
            "source": "SYSTEM",
            "url": ""
        }]

    newsletter_text = format_newsletter(items)

    file_path = create_ppt({
        "items": items
    })

    result = {
        "items": items,
        "newsletter_text": newsletter_text,
        "file_path": file_path
    }

    set_cache(result)

    return result
