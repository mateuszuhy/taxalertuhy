from legal_filter import is_tax_legal_event

def get_all_news():

    all_items = []

    for url, source in SOURCES:
        items = scrape(url, source)

        for i in items:

            if is_tax_legal_event(i["title"]):
                all_items.append(i)

    # dedupe
    seen = set()
    clean = []

    for i in all_items:
        if i["title"] not in seen:
            seen.add(i["title"])
            clean.append(i)

    return clean
