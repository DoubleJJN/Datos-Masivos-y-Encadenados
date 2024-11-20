#This script crawls the wikipedia page of countries and extracts the name of the country, the sovereign state and the capital of each country.
import requests
from bs4 import BeautifulSoup
import json
def get_countries():
    url = 'https://es.wikipedia.org/wiki/Anexo:Pa%C3%ADses'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'wikitable'})
    rows = table.find_all('tr')
    data = {}
    for row in rows[1:]:
        cols = row.find_all('td')
        try:
            soberan_state = cols[0].find_all('a')[1].text
            country = cols[0].find('small').text.replace('(', '').replace(')', '').replace('\n', '')
            capital = cols[2].text
            data[country] = {'soberan_state': soberan_state, 'capital': capital}
        except:
            # try:
            #     print(cols[0].find_all('a')[1].text)
            # except:
            #       print('No tiene nombre')
            pass
    return data

paises = get_countries()

with open('./blog/crawlers/data/paises.json', 'w', encoding="utf-8") as file:
    json.dump(paises, file, indent=4, ensure_ascii=False)