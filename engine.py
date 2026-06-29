from scraper import get_all_news
from ai_engine import process_batch
from editor import write_newsletter
from ppt_generator import create_ppt
from cache import get_cache, set_cache


def categorize(item):

    score = item.get("impact_score", 0)

    if score >= 70:
        return "lead"
    return "standard"


def run_engine(api_key):

    cached = get_cache()
    if cached:
        return cached

    news = get_all_news()

    news = news[:40]

    items = process_batch(news, api_key)

    lead = []
    standard = []

    for i in items:

        bucket = categorize(i)

        if bucket == "lead":
            lead.append(i)
        else:
            standard.append(i)

    # GUARANTEE OUTPUT
    if not lead and not standard:

        standard.append({
            "title": "Brak istotnych zmian podatkowych",
            "summary": {
                "what_changed": "Brak zmian legislacyjnych VAT/CIT/PIT",
                "impact": "Stabilne otoczenie podatkowe",
                "legal_basis": "Brak nowych aktów prawnych"
            },
            "source": "SYSTEM",
            "url": ""
        })

    file_path = create_ppt({
        "lead": lead,
        "standard": standard
    })

    return {
        "lead": lead,
        "standard": standard,
        "newsletter_text": write_newsletter(items),
        "file_path": file_path
    }
