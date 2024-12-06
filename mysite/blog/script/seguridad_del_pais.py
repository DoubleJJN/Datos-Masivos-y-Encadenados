import requests
import bs4

def obtener_datos_seguridad(pais):
    BASE_URL = "https://www.travelsafe-abroad.com/es/"
    response = requests.get(BASE_URL + pais)
    beautiful = bs4.BeautifulSoup(response.text, "html.parser")

    porcentaje = [i.text for i in beautiful.findAll("span", {"id": "percent"})]
    safety = [i.text for i in beautiful.findAll("div", {"class": "safety-index-box"})]
    user_sentiment = [i.text for i in beautiful.findAll("div", {"class": "user-sentiment-box"})]
    safety_city_green = [i.text for i in beautiful.findAll("a", {"class": "score-cell-color cell-color-green"})]
    safety_city_orange = [i.text for i in beautiful.findAll("a", {"class": "score-cell-color cell-color-orange"})]
    warnings = [k.text for j in beautiful.findAll("div", {"class": "warning-item"}) for k in j.findAll("h3", {"class": "anchor-heading clearfix"})]

    datos_seguridad = {
        "porcentaje": porcentaje,
        "safety": safety,
        "user_sentiment": user_sentiment,
        "safety_city_green": safety_city_green,
        "safety_city_orange": safety_city_orange,
        "warnings": warnings
    }

    return datos_seguridad