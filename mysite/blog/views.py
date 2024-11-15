from django.shortcuts import render, get_object_or_404
from django.http import StreamingHttpResponse, JsonResponse
from .models import Destination
from .utils import query_ollama, get_destination, get_all_destinations


def index(request):
    return render(request, "blog/index.html")


def search_destinations(request):
    query = request.GET.get("q")
    if query:
        results = Destination.objects.filter(name__icontains=query)  # Filter by name
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
