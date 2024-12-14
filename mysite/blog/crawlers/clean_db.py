import sqlite3
import requests
from tqdm import tqdm
from time import sleep



def clean(text: str) -> str:
    # remove any [n] from the text
    text = text.split("[")[0]
    return text


db_path = "db.sqlite3"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Leer los valores de la columna `name`
cursor.execute("SELECT * FROM blog_destination")
rows = cursor.fetchall()
print(f"Se encontraron {len(rows)} filas")
# Procesar cada fila y actualizar la columna `imgs`
for row in tqdm(rows[:]):
    cursor.execute(
        "UPDATE blog_destination SET currency = ?, language = ?, timezone = ? WHERE id = ?",
        (clean(row[5]), clean(row[6]), clean(row[7]), row[0]),
    )
    conn.commit()

# Guardar los cambios y cerrar la conexión
conn.close()

print("¡Columnas actualizadas con éxito!")
