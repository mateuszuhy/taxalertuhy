import requests
from bs4 import BeautifulSoup
from legal_filter import is_valid_tax_event


SOURCES = [
    ("https://www.prawo.pl/podatki", "PRAWO"),
    ("https://www.rp.pl/podatki", "RP"),
    ("https://www.gov.pl/web/finanse", "MF"),
    ("https://www.podatki.gov.pl", "TAX_GOV"),
    ("https://isap.sejm.gov.pl", "ISAP"),
    ("https://rcl.gov.pl", "RCL")
]


def scrape(url, source):

    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        items = []

        for a in soup.find_all("a"):
            title = a.get_text(strip=True)

            if title and len(title) > 40:
                if is_valid_tax_event(title):
                    items.append({
                        "title": title,
                        "source": source,
                        "url": url
                    })

        return items

    except:
        return []


def get_all_news():

    all_items = []

    for url, source in SOURCES:
        all_items += scrape(url, source)

    # dedupe
    seen = set()
    clean = []

    for i in all_items:
        if i["title"] not in seen:
            seen.add(i["title"])
            clean.append(i)

    return clean
