import requests
from bs4 import BeautifulSoup


# -----------------------------
# TAX DOMAIN FILTER
# -----------------------------
TAX_KEYWORDS = [
    "VAT", "CIT", "PIT", "podatek", "podatkowy",
    "Ordynacja podatkowa", "akcyz",
    "ustawa o podatku", "MF", "Minister Finansów",
    "ISAP", "Dz.U.", "danina"
]


def is_tax_related(text: str) -> bool:

    if not text:
        return False

    text_lower = text.lower()

    return any(k.lower() in text_lower for k in TAX_KEYWORDS)


# -----------------------------
# ISAP SCRAPER (FILTERED)
# -----------------------------
def scrape_isap():

    url = "https://isap.sejm.gov.pl"
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    news = []

    for a in soup.find_all("a"):

        t = a.get_text(strip=True)

        if len(t) > 40 and is_tax_related(t):

            news.append({
                "title": t,
                "source": "ISAP"
            })

    return news


# -----------------------------
# MF SCRAPER (FILTERED)
# -----------------------------
def scrape_mf():

    url = "https://www.gov.pl/web/finanse"
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    news = []

    for a in soup.find_all("a"):

        t = a.get_text(strip=True)

        if len(t) > 40 and is_tax_related(t):

            news.append({
                "title": t,
                "source": "MF"
            })

    return news


# -----------------------------
# FINAL NEWS PIPELINE
# -----------------------------
def get_all_news():

    isap = scrape_isap()
    mf = scrape_mf()

    combined = isap + mf

    # final safety filter
    return [n for n in combined if is_tax_related(n["title"])]
