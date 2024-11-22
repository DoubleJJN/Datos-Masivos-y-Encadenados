from django.shortcuts import render, get_object_or_404
from django.http import StreamingHttpResponse, JsonResponse
from django.db.models import Q
from .models import Destination
from .utils import query_ollama, get_destination, get_all_destinations
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "blog/index.html")


def search_destinations(request):
    query = request.GET.get("q")
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    #clean query and remove any special characters
    print("Query is", query)
    print("Start date is", start_date)
    print("End date is", end_date)

    # Guardar las fechas en la sesión del usuario
    request.session['start_date'] = start_date
    request.session['end_date'] = end_date

    query = ''.join(e for e in query.strip().lower() if e.isalnum())
    if query:
        results = Destination.objects.filter(Q(name__icontains=query) | Q(english_name__icontains=query))
        if results:
            results = results[0]
            results.image_url = results.image_url.split(",")
        else:
            results = get_destination(query)
        # results = Destination.objects.none()  # No results if no query
    # print(results)
    
    return render(
        request, "blog/destinations.html", {"results": results, "query": query}
    )


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
