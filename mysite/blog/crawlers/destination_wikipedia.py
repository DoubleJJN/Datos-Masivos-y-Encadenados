from bs4 import BeautifulSoup
import requests
import unicodedata
import json
import re
from .crawler import Crawler
from ..env import API_KEY



class WikipediaCrawler(Crawler):
    def __init__(self):
        super().__init__(
            "WikipediaDestinationCrawler", "https://es.wikipedia.org/wiki/"
        )

    def get_country_data(self, country: str) -> dict:
        soup = self.crawl(country)
        data = {
            "currency": None,
            "language": None,
        }
        try:
            infobox = soup.find("table", class_="infobox")
        except AttributeError:
            print(f"Error al obtener datos de {country}")
        if infobox:
            rows = infobox.find_all("tr")
            for row in rows:
                header = row.find("th")
                value = row.find("td")
                if not header or not value:
                    continue
                header_text = header.text.strip().lower()
                if "moneda" in header_text:
                    data["currency"] = self.clean_text(value.text.strip())
                if "idioma" in header_text:
                    data["language"] = self.clean_text(value.text.strip())
                if "huso horario" in header_text or "timezone" in header_text:
                    data["timezone"] = self.clean_text(value.text.strip())
        # print("data retrieved")
        return data

    def clean_text(self, text: str) -> str:
        text = unicodedata.normalize("NFKC", text)

        text = re.sub(r"[\u200b-\u200d\u2060-\u206f]", "", text)

        text = re.sub(r"\s+", " ", text).strip()

        return text

    def get_imgs(self, place_english: str) -> str:
        photos = []
        URL = "https://api.pexels.com/v1/search"
        headers = {"Authorization": API_KEY}
        params = {"query": place_english, "per_page": 3, "orientation": "landscape"}
        response = requests.get(URL, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            if data["photos"]:
                for i, photo in enumerate(data["photos"], start=1):
                    photos.append(photo["src"]["original"])
        return ",".join(photos)

    def get_data(self, place: str, place_english: str) -> dict:
        """
        Extracts important information about a destination from a Wikipedia page.
        """
        soup = self.crawl(place)

        data = {
            "name": None,
            "english_name": place_english,
            "country": None,
            "description": None,
            "image_url": None,
        }

        # Extracting the title of the page (name of the destination)
        title = soup.find("h1", id="firstHeading")
        if title:
            data["name"] = title.text.strip()

        # Extracting a brief description (first paragraph in content)
        description = soup.find("div", class_="mw-content-ltr")
        if description:
            first_paragraph = description.find(
                "p",
                recursive=False,
                class_=lambda x: x != "mw-empty-elt" if x else True,
            )
            if first_paragraph:
                # Quitamos los saltos de línea, espacios en blanco y corchetes
                text = re.sub(r"\s+", " ", first_paragraph.text).strip()
                text = text.replace("\n", " ")
                text = re.sub(r"\[.*?\]", "", text)
                data["description"] = self.clean_text(text)

        # Extracting the country, language, currency, and timezone from the infobox
        infobox = soup.find("table", class_="infobox")
        if infobox:
            rows = infobox.find_all("tr")
            for row in rows:
                header = row.find("th")
                value = row.find("td")
                if not header or not value:
                    continue
                header_text = header.text.strip().lower()
                if header_text.strip() == "país" or header_text.strip() == "• país":
                    try:
                        data["country"] = self.clean_text(
                            value.find("a", recursive=False).text.strip()
                        )
                    except Exception:
                        print(f"Error al obtener el país de {place}")
            if not data["country"]:
                data["country"] = place
            data = data | self.get_country_data(data["country"])
            data["image_url"] = self.get_imgs(place_english)
        # print(f"data retrieved from {place}")
        return data


# crawler = WikipediaCrawler()
# print(crawler.get_data("El Cairo", "Cairo"))
