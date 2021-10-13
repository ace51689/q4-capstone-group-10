from django.urls import path, include 
from . import views
from . import Models

urlpatterns = [
    path('posts/', include('posts.urls')),
    ]