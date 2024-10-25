from django.urls import path
from . import views

urlpatterns = [
    path('blog/', views.index, name='blog_posts'),
    path('blog/<int:post_id>/', views.post_detail, name='post_detail'),
]