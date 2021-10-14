from django.urls import path, include 
from . import views


urlpatterns = [
    path('posts/', include('posts.urls')),
    ]