from django.shortcuts import render
from .models import Post

def index(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(title__icontains=query)  # Filtra los posts que contienen la consulta en el título
    else:
        posts = Post.objects.all()
    return render(request, 'blog/index.html', {'posts': posts})