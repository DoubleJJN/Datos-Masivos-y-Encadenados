from django.urls import path
from . import views

urlpatterns = [
    # path('/', views.index, name='Travelia'),
    path("search/", views.search_destinations, name="search_destinations"),
    path("ollama-query/", views.query_ollama, name="query_ollama"),
    path("get-flights/", views.get_flights, name="get_flights"),
    # path('blog/<int:post_id>/', views.post_detail, name='post_detail'),
]
