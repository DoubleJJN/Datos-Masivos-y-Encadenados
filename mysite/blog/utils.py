import requests
import json
from string import Template
from .crawlers.destination_wikipedia import WikipediaCrawler
from .crawlers.crawl_all_destinations import crawl_destinations
from .models import Destination

query_template = Template(
    "Describe en dos frases en texto plano $destino para un turista que visita por primera vez."
)


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
        if query
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
