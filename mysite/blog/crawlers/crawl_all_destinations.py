from concurrent.futures import ThreadPoolExecutor, as_completed
from .destination_wikipedia import WikipediaCrawler
import json
import traceback
from tqdm import tqdm


def process_place(crawler, place):
    try:
        # print(f"Processing {place}...")
        data = crawler.get_data(place)
        crawler.save_to_db(data)
        # print(f"Data for {place} saved successfully.")
    except Exception as e:
        print(f"Error processing {place}: {e}")
        traceback.print_exc()
        return {place: None}

def crawl_destinations():
    with open('paises.json', 'r', encoding='utf-8') as file:
        countries = json.load(file)
    places = [country for country in countries.keys()]
    capital = [country['capital'] for country in countries.values()]
    places.extend(capital)
    
    # Instancia del crawler
    crawler = WikipediaCrawler()

    # Usamos ThreadPoolExecutor para procesar múltiples lugares simultáneamente
    results = {}
    with ThreadPoolExecutor(max_workers=8) as executor:  # Ajusta max_workers según los recursos disponibles
        futures = {executor.submit(process_place, crawler, place): place for place in places}

        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing destinations"):
            pass
