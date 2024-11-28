from django.shortcuts import render, get_object_or_404
from django.http import StreamingHttpResponse, JsonResponse
from django.db.models import Q
from .models import Destination
from .utils import query_ollama, get_destination, get_all_destinations, get_flights_list
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "blog/index.html")


def search_destinations(request):
    query = request.GET.get("q")
    departure_date = request.GET.get("departure_date")
    return_date = request.GET.get("return_date")
    num_people = request.GET.get("num_people")
    # clean query and remove any special characters
    print("Query is", query)
    print("Start date is", departure_date)
    print("End date is", return_date)
    print("Number of people is", num_people)

    # Guardar las fechas en la sesión del usuario
    request.session["arrival_date"] = departure_date
    request.session["departure_date"] = return_date

    query = "".join(e for e in query.strip().lower() if e.isalnum())
    if query:
        results = Destination.objects.filter(
            Q(name__icontains=query) | Q(english_name__icontains=query)
        )
        if results:
            results = results[0]
            results.image_url = results.image_url.split(",")
        else:
            results = get_destination(query)

    return render(
        request, "blog/destinations.html", {"results": results, "query": query}
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
