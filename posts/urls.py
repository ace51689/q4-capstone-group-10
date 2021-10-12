from django.urls import path, include
from . import views
from . import Models

urlpatterns = [
    path('Posts/', include('Posts.urls')),
    ]
