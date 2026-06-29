import requests
from bs4 import BeautifulSoup


TAX_KEYWORDS = [
    "VAT", "CIT", "PIT", "akcyz", "podatek",
    "ustawa podatkowa", "Ordynacja podatkowa",
    "MF", "Minister Finansów",
    "ISAP", "Dz.U."
]


def is_tax_related(text):

    text_lower = text.lower()

    return any(k.lower() in text_lower for k in TAX_KEYWORDS)


def scrape_isap():

    url = "https://isap.sejm.gov.pl"
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    news = []

    for a in soup.find_all("a"):

        t = a.get_text(strip=True)

        if len(t) > 30 and is_tax_related(t):

            news.append({
                "title": t,
                "source": "ISAP"
            })

    return news


def scrape_mf():

    url = "https://www.gov.pl/web/finanse"
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    news = []

    for a in soup.find_all("a"):

        t = a.get_text(strip=True)

        if len(t) > 30 and is_tax_related(t):

            news.append({
                "title": t,
                "source": "MF"
            })

    return news


def get_all_news():

    return scrape_isap() + scrape_mf()
