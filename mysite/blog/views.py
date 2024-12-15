from django.shortcuts import render, get_object_or_404
from django.http import StreamingHttpResponse, JsonResponse
from django.db.models import Q
from .models import Destination
from .utils import (
    query_ollama,
    get_destination,
    get_all_destinations,
    get_flights_list,
    get_hotel_list,
)
from django.shortcuts import render
from django.http import HttpResponse
from difflib import SequenceMatcher
from .script.seguridad_del_pais import obtener_datos_seguridad  # type: ignore # Importa la función
import requests


def index(request):
    return render(request, "blog/index.html")


def search_destinations(request):
    query = request.GET.get("q")
    departure_date = request.GET.get("departure_date")
    return_date = request.GET.get("return_date")
    num_people = request.GET.get("num_people")

    # Limpiar y procesar la consulta
    query = query.strip().lower() if query else ""

    # Guardar las fechas en la sesión del usuario
    request.session["arrival_date"] = departure_date
    request.session["departure_date"] = return_date

    # Retirar caracteres especiales
    query = "".join(e for e in query if e.isalnum())

    results = None
    if query:
        all_destinations = Destination.objects.all()

        # Calcular similitudes con difflib
        def similarity(a, b):
            return SequenceMatcher(None, a, b).ratio()

        # Crear una lista con las similitudes
        scored_results = [
            (
                dest,
                max(
                    similarity(query, dest.name.lower()),
                    similarity(query, dest.english_name.lower()),
                ),
            )
            for dest in all_destinations
        ]

        # Ordenar resultados por similitud descendente
        scored_results = sorted(scored_results, key=lambda x: x[1], reverse=True)

        # Seleccionar el destino más similar si existe
        if scored_results and scored_results[0][1] > 0.3:  # Umbral de similitud
            results = scored_results[0][0]
            results.image_url = results.image_url.split(",")
        else:
            results = get_destination(query)

        datos_seguridad = obtener_datos_seguridad(query)

        query_info = {}
        query_info["departure_date"] = departure_date
        query_info["return_date"] = return_date
        query_info["num_people"] = num_people
        print(query_info)

    return render(
        request,
        "blog/destinations.html",
        {
            "results": results,
            "query": query,
            "corrected_place": results.name,
            "query_info": query_info,
            "datos_seguridad": datos_seguridad,
        },
    )


def get_flights_api(request):
    departure = request.GET.get("departure")
    destination = request.GET.get("q")
    departure_date = request.GET.get("departure_date")
    return_date = request.GET.get("return_date")
    num_people = request.GET.get("num_people")
    flights = get_flights_list(
        departure, destination, departure_date, return_date, num_people
    )
    return JsonResponse({"flights": flights})


def get_hotels_api(request):
    hotels_list = get_hotel_list()
    return JsonResponse({"hotels": hotels_list})


def ollama(request):
    return render(request, "blog/ollama.html")


def ollama_query_api(request):
    query = request.GET.get("query")
    # print(query)
    context = query_ollama(query)
    return JsonResponse(context)


def get_all_destinations_v(request):
    results = get_all_destinations()
    return results


def map(request):
    MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoibWF0enVsbCIsImEiOiJjbTRjbnhjNGYwNzZwMmxxcDdhcjNkenJqIn0.j1gK6McQfLPZNT84sbi_yw"
    place = request.GET.get("place")
    return render(
        request,
        "blog/map.html",
        {"mapbox_access_token": MAPBOX_ACCESS_TOKEN, "country": place},
    )
