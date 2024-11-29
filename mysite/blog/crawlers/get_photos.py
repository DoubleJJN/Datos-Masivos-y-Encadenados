import sqlite3
import requests
from tqdm import tqdm
from time import sleep
API_KEY = 'jeXvP9Un4E2RpgrYJYZFRB8XAMCMiuyVOY9fv6DHY5BZoR08HVghIbMS'

def get_imgs(place_english: str) -> str:
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
        elif response.status_code == 429:
            # print("API limit reached")
            sleep(5)
            return get_imgs(place_english)
        return ",".join(photos)

db_path = "db.sqlite3"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Leer los valores de la columna `name`
cursor.execute("SELECT id, english_name FROM blog_destination WHERE image_url IS NULL OR image_url = ''")
rows = cursor.fetchall()
print(f"Se encontraron {len(rows)} filas")
# Procesar cada fila y actualizar la columna `imgs`
for row in tqdm(rows[:]):
    row_id, name = row
    imgs = get_imgs(name)
    cursor.execute("UPDATE blog_destination SET image_url = ? WHERE id = ?", (imgs, row_id))
    conn.commit()

# Guardar los cambios y cerrar la conexión
conn.close()

print("¡Columna 'imgs' actualizada con éxito!")