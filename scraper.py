import requests
from bs4 import BeautifulSoup


# -----------------------------
# SOURCE TIERS
# -----------------------------
PRIMARY_SOURCES = ["isap.sejm.gov.pl", "eli.gov.pl"]
GOV_SOURCES = ["gov.pl", "podatki.gov.pl"]
COMMENTARY_SOURCES = ["prawo.pl", "rp.pl"]


def scrape_generic(url, source):

    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        items = []

        for a in soup.find_all("a"):

            t = a.get_text(strip=True)

            if len(t) > 40:

                items.append({
                    "title": t,
                    "source": source,
                    "url": url
                })

        return items

    except:
        return []


def get_all_news():

    # PRIMARY LAW (highest value)
    isap = scrape_generic("https://isap.sejm.gov.pl", "ISAP")
    eli = scrape_generic("https://eli.gov.pl", "ELI")

    # GOV GUIDANCE
    mf = scrape_generic("https://www.gov.pl/web/finanse", "MF")
    taxgov = scrape_generic("https://www.podatki.gov.pl", "TAX GOV")

    # COMMENTARY
    rp = scrape_generic("https://www.rp.pl/podatki", "RP")
    prawo = scrape_generic("https://www.prawo.pl/podatki", "PRAWO.PL")

    return isap + eli + mf + taxgov + rp + prawo
