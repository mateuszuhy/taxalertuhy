import requests
from bs4 import BeautifulSoup


# -----------------------------
# CONTROLLED SOURCES (LESS NOISE)
# -----------------------------
SOURCES = [
    ("https://isap.sejm.gov.pl", "ISAP"),
    ("https://www.gov.pl/web/finanse", "MF"),
    ("https://www.podatki.gov.pl", "TAX GOV"),
    ("https://www.prawo.pl/podatki", "PRAWO.PL"),
    ("https://www.rp.pl/podatki", "RP.PL")
]


def scrape(url, source):

    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        items = []

        for a in soup.find_all("a"):

            t = a.get_text(strip=True)

            if t and len(t) > 40:

                items.append({
                    "title": t,
                    "source": source
                })

        return items

    except:
        return []


def get_all_news():

    all_items = []

    for url, source in SOURCES:
        all_items += scrape(url, source)

    # dedup early
    seen = set()
    unique = []

    for i in all_items:
        if i["title"] not in seen:
            seen.add(i["title"])
            unique.append(i)

    return unique
