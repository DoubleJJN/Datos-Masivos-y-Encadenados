from bs4 import BeautifulSoup
import requests
import unicodedata
import json
import re
from .crawler import Crawler


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
        infobox = soup.find("table", class_="infobox")
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
                if "idioma oficial" in header_text:
                    data["language"] = self.clean_text(value.text.strip())
                if "huso horario" in header_text or "timezone" in header_text:
                    data["timezone"] = self.clean_text(value.text.strip())
        return data

    def clean_text(self, text: str) -> str:
        text = unicodedata.normalize("NFKC", text)

        text = re.sub(r"[\u200b-\u200d\u2060-\u206f]", "", text)

        text = re.sub(r"\s+", " ", text).strip()

        return text

    def get_data(self, place: str) -> dict:
        """
        Extracts important information about a destination from a Wikipedia page.
        """
        soup = self.crawl(place)

        data = {"name": None, "country": None, "description": None, "image_url": None}

        # Extracting the title of the page (name of the destination)
        title = soup.find("h1", id="firstHeading")
        if title:
            data["name"] = title.text.strip()

        # Extracting a brief description (first paragraph in content)
        description = soup.find("div", class_="mw-content-ltr")
        if description:
            first_paragraph = description.find("p")
            if first_paragraph:
                # Quitamos los saltos de línea, espacios en blanco y corchetes
                text = re.sub(r"\s+", " ", first_paragraph.text).strip()
                text = text.replace("\n", " ")
                text = re.sub(r"\[.*?\]", "", text)
                data["description"] = self.clean_text(text)

        # Extracting the country, language, currency, and timezone from the infobox
        infobox = soup.find("table", class_="infobox")
        if infobox:
            imgs = ",".join(
                [
                    "https:" + re.sub(r"\d+px", "1920px", img["src"])
                    for img in infobox.find_all("img")
                    if img["src"].endswith("jpg")
                ]
            )
            if imgs:
                data["image_url"] = imgs
            rows = infobox.find_all("tr")
            for row in rows:
                header = row.find("th")
                value = row.find("td")
                if not header or not value:
                    continue
                header_text = header.text.strip().lower()
                if "país" in header_text:
                    data["country"] = self.clean_text(value.text.strip())
            data = data | self.get_country_data(data["country"])
        return data
