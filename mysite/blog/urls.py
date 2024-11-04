from django.urls import path
from . import views

urlpatterns = [
    # path('/', views.index, name='Travelia'),
    path('search/', views.search_destinations, name='search_destinations')
    # path('blog/<int:post_id>/', views.post_detail, name='post_detail'),
]