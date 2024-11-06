from django.shortcuts import render, get_object_or_404
from .models import Destination
# from .models import Post

def index(request):
    # query = request.GET.get('q')
    # if query:
    #     posts = Post.objects.filter(title__icontains=query)  # Filtra los posts que contienen la consulta en el título
    # else:
    #     posts = Post.objects.all()
    return render(request, 'blog/index.html')#, {'posts': posts})

def search_destinations(request):
    query = request.GET.get('q')
    if query:
        results = Destination.objects.filter(name__icontains=query)  # Filter by name
    else:
        results = Destination.objects.none()  # No results if no query
    return render(request, 'blog/destinations.html', {'results': results, 'query': query})