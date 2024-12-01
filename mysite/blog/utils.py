import requests
import json
from string import Template
from .crawlers.destination_wikipedia import WikipediaCrawler
from .crawlers.crawl_all_destinations import crawl_destinations
from .models import Destination
from .crawlers.flights_scrapper import FlightsScrapper
import random
import os

query_template = Template(
    "Describe en dos frases en texto plano $destino para un turista que visita por primera vez."
)

flights_scrapper = FlightsScrapper()


def get_text(responses):
    text = ""
    for response in responses.decode("utf-8", "ignore").split("\n")[:-1]:
        try:
            nresponse = json.loads(response)
            text += nresponse.get("response", "")
        except json.JSONDecodeError as e:
            print("Error parsing JSON:", response, e)
    # print(text)
    return text


def query_ollama(query):
    query = (
        query_template.substitute(destino=query)
        if query and query.isalpha()
        else query_template.substitute(destino="París")
    )
    # 192.168.0.11
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {"model": "phi3", "prompt": query, "streaming": "False"}
    print(query)
    try:
        # Realizar la solicitud al servidor de Ollama
        data = json.dumps(data)
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            result = get_text(response.content)
        else:
            result = "Error Occurred:", response.text
        context = {"result": result}
    except requests.RequestException as e:
        context = {"error": f"Error al conectar con Ollama: {e}"}

    return context


# gets a destination from the database or crawls it if it doesn't exist
def get_destination(destination):
    try:
        destination_data = Destination.objects.get(name=destination)
        return destination_data
    except Destination.DoesNotExist:
        pass
    destination_crawler = WikipediaCrawler()
    data = destination_crawler.get_data(destination)
    destination_crawler.save_to_db(data)
    return data


def get_all_destinations():
    crawl_destinations()
    return "Crawling completed successfully."


# gets a list of flights from the user data in real time
def get_flights_list(departure, arrival, departure_date, arrival_date, num_people):
    try:
        flights_list = flights_scrapper.scrape(
            departure, arrival, departure_date, arrival_date, num_people
        )
        return flights_list
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_hotel_list():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "crawlers", "data")
    with open(os.path.join(data_path, "commodities.txt"), "r") as f:
        commodities = f.read().split("\n")
    with open(os.path.join(data_path, "hotels.txt"), "r") as f:
        hotels = f.read().split("\n")

    # construct a list of hotels with random prices and random ratings getting from 1 to 5 commodities per hotel
    hotels_list = []
    for hotel in random.sample(hotels, random.randint(3, 6)):
        if not hotel.strip():  # Asegurar que el nombre no está vacío
            continue
        price = round(random.uniform(70, 150), 2)  # Precio entre 30 y 500
        rating = round(random.uniform(4, 5), 1)  # Calificación entre 1 y 5
        # Seleccionar de 1 a 5 comodidades
        selected_commodities = random.sample(commodities, random.randint(1, 5))
        hotel_entry = {
            "HotelName": hotel,
            "PricePerNight": price,
            "Rating": rating,
            "Commodities": selected_commodities,
        }
        hotels_list.append(hotel_entry)
    return hotels_list
