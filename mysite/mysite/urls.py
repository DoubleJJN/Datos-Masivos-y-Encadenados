"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from blog import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="home"),  # Add this line to handle the empty path
    path("search/", views.search_destinations, name="search_destinations"),
    path("ollama/", views.ollama, name="ollama"),
    path("search/api/ollama_query/", views.ollama_query_api, name="query_ollama_api"),
    path(
        "search/api/get_all_destinations/",
        views.get_all_destinations_v,
        name="get_all_destinations",
    ),
    path("search/api/get_flights/", views.get_flights_api, name="get_flights"),
    path("search/api/get_hotels/", views.get_hotels_api, name="get_hotels"),
    path("map/", views.map, name="map"),
    # path('blog/', include('blog.urls')),
]
