import requests

API_KEY = 'jeXvP9Un4E2RpgrYJYZFRB8XAMCMiuyVOY9fv6DHY5BZoR08HVghIbMS'

URL = "https://api.pexels.com/v1/search"

place = "Madrid"

headers = {
    "Authorization": API_KEY
}

params = {
    'query': place,
    'per_page': 3
}

response = requests.get(URL, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    if data['photos']:
        for i, photo in enumerate(data['photos'], start=1):
            photo_url = photo['src']['original']
            print(f"Foto {i} URL:", photo_url)
    else:
        print(f"No se encontraron fotos para el lugar: {place}")
else:
    print(f"Error {response.status_code}: No se pudo obtener la información.")
