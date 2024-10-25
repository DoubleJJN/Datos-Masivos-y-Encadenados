from django.shortcuts import render, get_object_or_404
from .models import Post

def index(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(title__icontains=query)  # Filtra los posts que contienen la consulta en el título
    else:
        posts = Post.objects.all()
    return render(request, 'blog/index.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})