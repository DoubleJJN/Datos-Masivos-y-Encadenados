# Define the base class crawler with the following methods:
# - crawl: a method that takes a url and returns the html content of the page
# - get_text: a method that takes the html content of a page and returns the text content
# - get_data: a method that takes the html content of a page and returns a dictionary of data in the page
# - the class must handle the appropriate exceptions
# - the get_data method must be implemented by the subclasses

import requests
import json
import json.decoder
from typing import List, Dict
from bs4 import BeautifulSoup
from ..models import Destination


class Crawler:
    def __init__(self, name: str, base_url: str):
        self.name = name
        self.base_url = base_url

    def crawl(self, params) -> BeautifulSoup:
        if not params:
            return None
        try:
            response = requests.get(self.base_url + params)
            response.raise_for_status()
            self.soup = self.get_soup(response.text)
            # print(f"Fetching data from {self.base_url + params}...")
            return self.soup
        except requests.exceptions.RequestException as e:
            print(e)
            return None

    def get_soup(self, html: str) -> BeautifulSoup:
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def get_data(self, html: str) -> dict:
        raise NotImplementedError

    def save_to_db(self, data: Dict):
        try:
            destination = Destination(
                name=data.get("name"),
                english_name=data.get("english_name"),
                country=data.get("country"),
                description=data.get("description"),
                currency=data.get("currency"),
                language=data.get("language"),
                timezone=data.get("timezone"),
                image_url=data.get("image_url"),
            )
            destination.save()
            # print(f"Destino {destination.name} guardado con éxito en la base de datos.")
        except Exception as e:
            name = data.get("name")
            print(f"Error al guardar {name} en la base de datos: {e}")
