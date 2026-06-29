import requests
from bs4 import BeautifulSoup


def scrape_mf():

    url = "https://www.gov.pl/web/finanse"
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    news = []

    for a in soup.find_all("a"):
        t = a.get_text(strip=True)

        if len(t) > 40:
            news.append({"title": t, "source": "MF"})

    return news


def scrape_isap():

    url = "https://isap.sejm.gov.pl"
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    news = []

    for a in soup.find_all("a"):
        t = a.get_text(strip=True)

        if "Dz.U." in t or "ustawa" in t.lower():
            news.append({"title": t, "source": "ISAP"})

    return news


def get_all_news():

    return scrape_mf() + scrape_isap()
