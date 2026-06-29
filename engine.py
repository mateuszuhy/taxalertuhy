from scraper import get_all_news
from ai_engine import process_batch
from editor import format_newsletter
from ppt_generator import create_ppt
from cache import get_cache, set_cache
from schema import TaxItem


def normalize(items):

    clean = []

    for i in items:

        clean.append(TaxItem(
            title=i.get("title", ""),
            what_changed=i.get("what_changed", ""),
            impact=i.get("impact", ""),
            legal_basis=i.get("legal_basis", ""),
            source=i.get("source", ""),
            url=i.get("url", "")
        ))

    return clean


def run_engine(api_key):

    cached = get_cache()
    if cached:
        return cached

    news = get_all_news()
    news = news[:40]

    items_raw = process_batch(news, api_key)

    items = normalize(items_raw)

    # fallback safety
    if not items:
        items = [TaxItem(
            title="Brak istotnych zmian podatkowych",
            what_changed="Nie zidentyfikowano zmian legislacyjnych VAT/CIT/PIT",
            impact="Stabilne otoczenie podatkowe",
            legal_basis="Brak nowych aktów prawnych",
            source="SYSTEM",
            url=""
        )]

    newsletter_text = format_newsletter(items)

    file_path = create_ppt(items)

    result = {
        "items": items,
        "newsletter_text": newsletter_text,
        "file_path": file_path
    }

    set_cache(result)

    return result
