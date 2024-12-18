from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import traceback
import json
import os
from time import time_ns


class Cache:
    def __init__(self, minutes=5):
        self.cache = {}
        self.minutes = minutes

    def simple_hash(self, key):
        return str(sum([ord(c) for c in key])) + str(len(key))

    def check_keys_timestamp(self):
        for key, data in self.cache.items():
            if (time_ns() - data["timestamp"]) / 1e9 / 60 > self.minutes:
                del self.cache[key]

    def get(self, key):
        self.check_keys_timestamp()
        key = self.simple_hash(key)
        if key in self.cache.keys():
            data = self.cache[key]
            return data["data"]
        return None

    def set(self, key, data):
        key = self.simple_hash(key)
        self.cache[key] = {"data": data, "timestamp": time_ns()}
        self.print_cache()

    def print_cache(self):
        for key, data in self.cache.items():
            print(key)

    def clear(self):
        self.cache = {}


class FlightsScrapper:
    def __init__(self):
        self.base_url = "https://flights.booking.com/flights"
        self.headless = True
        self.options = Options()
        if self.headless:
            self.options.add_argument("--headless")
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--no-sandbox")
            self.options.add_argument("--disable-dev-shm-usage")

        # Ruta absoluta basada en la ubicación de flights_scrapper.py
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Construye la ruta al JSON
        json_path = os.path.join(base_dir, "data", "airports.json")
        # Cargar la base de datos de aeropuertos
        with open(json_path, "r", encoding="utf-8") as f:
            self.airports_data = json.load(f)

        self.cache = Cache(5)

    def get_airport_by_city(city_name, airports_data):
        for airport in airports_data:
            if airport["city"].lower() == city_name.lower():
                return airport
        return None

    def get_airports_by_country(country_name, airports_data):
        for airport in airports_data:
            if airport["country"].lower() == country_name.lower():
                return airport
        return None

    # Construir la URL de búsqueda

    def url_builder(
        self, departure_city, arrival_city, num_people: str, departure_date, return_date
    ):
        departure_airport = FlightsScrapper.get_airport_by_city(
            departure_city, self.airports_data
        )
        arrival_airport = FlightsScrapper.get_airport_by_city(
            arrival_city, self.airports_data
        )
        if not arrival_airport:
            arrival_airport = FlightsScrapper.get_airports_by_country(
                arrival_city, self.airports_data
            )

        if not departure_airport or not arrival_airport:
            raise ValueError(
                "No se encontraron aeropuertos para las ciudades proporcionadas."
            )

        departure_iata = departure_airport["IATA"]
        arrival_iata = arrival_airport["IATA"]
        departure_name = departure_airport["airport"].replace(" ", "+")
        arrival_name = arrival_airport["airport"].replace(" ", "+")
        if not num_people.isnumeric() or int(num_people) > 4 or int(num_people) < 1:
            num_people = 1
        if not departure_date:
            departure_date = "2025-01-04"
        if not return_date:
            return_date = "2025-01-11"
        print(departure_iata, arrival_iata)
        print(departure_name, arrival_name)

        return f"{self.base_url}/{departure_iata}.AIRPORT-{arrival_iata}.AIRPORT/?type=ROUNDTRIP&adults={num_people}&cabinClass=ECONOMY&children=&from={departure_iata}.AIRPORT&to={arrival_iata}.AIRPORT&fromCountry=&toCountry=&fromLocationName={departure_name}&toLocationName={arrival_name}&depart={departure_date}&return={return_date}&sort=BEST"

    # Iniciar la busqueda en booking.com

    def scrape(
        self, departure_city, arrival_city, departure_date, return_date, num_people
    ):
        # Iniciar el navegador
        url = self.url_builder(
            departure_city, arrival_city, num_people, departure_date, return_date
        )
        if elems := self.cache.get(url):
            return self.cache.get(url)

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=self.options
        )
        try:
            # print(url)
            self.driver.get(url)
            wait = WebDriverWait(self.driver, 30)
            wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "ul[class*='List-module__root']")
                )
            )
            # print("Página cargada")
            # Extraer la información
            flights_data = []

            # Seleccionar todos los elementos <li> dentro del <ul>
            flights = self.driver.find_elements(
                By.CSS_SELECTOR,
                "ul[class*='List-module__root'] li[class*='List-module__item']",
            )

            for flight in flights[: min(5, len(flights))]:
                try:
                    flight_info = self.get_data(flight)
                    flights_data.append(flight_info)

                except Exception as e:
                    print(f"Error extrayendo datos de un vuelo: {e}")

        except Exception as e:
            print("Ocurrió un error:")
            traceback.print_exc()
            print(e)

        finally:
            self.driver.quit()
        self.cache.set(url, flights_data)
        return flights_data

    def get_data(self, flight):
        # Fechas y horas de salida/llegada (ida y vuelta)

        vuelo_ida_hora_salida = flight.find_element(
            By.CSS_SELECTOR, "[data-testid*='flight_card_segment_departure_time_0']"
        ).text
        vuelo_ida_lugar = flight.find_element(
            By.CSS_SELECTOR, "[data-testid*='flight_card_segment_departure_airport_0']"
        ).text
        vuelo_ida_fecha = flight.find_element(
            By.CSS_SELECTOR, "[data-testid*='flight_card_segment_departure_date_0']"
        ).text
        vuelo_ida_duracion = flight.find_element(
            By.CSS_SELECTOR, "[data-testid*='flight_card_segment_duration_0']"
        ).text
        vuelo_ida_hora_llegada = flight.find_element(
            By.CSS_SELECTOR, "[data-testid*='flight_card_segment_destination_time_0']"
        ).text
        vuelo_ida_lugar_llegada = flight.find_element(
            By.CSS_SELECTOR,
            "[data-testid*='flight_card_segment_destination_airport_0']",
        ).text
        vuelo_ida_fecha_llegada = flight.find_element(
            By.CSS_SELECTOR, "[data-testid*='flight_card_segment_destination_date_0']"
        ).text

        vuelo_vuelta_hora_salida = flight.find_element(
            By.CSS_SELECTOR, "[data-testid*='flight_card_segment_departure_time_1']"
        ).text
        vuelo_vuelta_lugar = flight.find_element(
            By.CSS_SELECTOR, "[data-testid*='flight_card_segment_departure_airport_1']"
        ).text
        vuelo_vuelta_fecha = flight.find_element(
            By.CSS_SELECTOR, "[data-testid*='flight_card_segment_departure_date_1']"
        ).text
        vuelo_vuelta_duracion = flight.find_element(
            By.CSS_SELECTOR, "[data-testid*='flight_card_segment_duration_1']"
        ).text
        vuelo_vuelta_hora_llegada = flight.find_element(
            By.CSS_SELECTOR, "[data-testid*='flight_card_segment_destination_time_1']"
        ).text
        vuelo_vuelta_lugar_llegada = flight.find_element(
            By.CSS_SELECTOR,
            "[data-testid*='flight_card_segment_destination_airport_1']",
        ).text
        vuelo_vuelta_fecha_llegada = flight.find_element(
            By.CSS_SELECTOR, "[data-testid*='flight_card_segment_destination_date_1']"
        ).text

        # Precios
        precio_individual = flight.find_element(
            By.CSS_SELECTOR, "[data-testid*='flight_card_price_main_price']"
        ).text
        precio_total = flight.find_element(
            By.CSS_SELECTOR, "[data-testid*='flight_card_price_total_price']"
        ).text

        # Aerolínea

        # Almacenar los datos en un diccionario
        flight_info = {
            "precio_individual": precio_individual,
            "precio_total": precio_total,
            "vuelo_ida": {
                "hora_salida": vuelo_ida_hora_salida,
                "lugar_salida": vuelo_ida_lugar,
                "fecha_salida": vuelo_ida_fecha,
                "duracion": vuelo_ida_duracion,
                "hora_llegada": vuelo_ida_hora_llegada,
                "lugar_llegada": vuelo_ida_lugar_llegada,
                "fecha_llegada": vuelo_ida_fecha_llegada,
            },
            "vuelo_vuelta": {
                "hora_salida": vuelo_vuelta_hora_salida,
                "lugar_salida": vuelo_vuelta_lugar,
                "fecha_salida": vuelo_vuelta_fecha,
                "duracion": vuelo_vuelta_duracion,
                "hora_llegada": vuelo_vuelta_hora_llegada,
                "lugar_llegada": vuelo_vuelta_lugar_llegada,
                "fecha_llegada": vuelo_vuelta_fecha_llegada,
            },
        }

        return flight_info


# ejemplo de uso
if __name__ == "__main__":
    scrapper = FlightsScrapper()
    data = scrapper.scrape("Madrid", "londres", "2024-12-21", "2024-12-28", "2")
    print(data)
