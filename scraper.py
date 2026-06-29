import requests
from bs4 import BeautifulSoup

def get_news():

    url = "https://www.gov.pl/web/finanse"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    news = []

    for a in soup.find_all("a"):

        title = a.get_text(strip=True)

        if len(title) > 40:
            news.append({"title": title})

    return news
