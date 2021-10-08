"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
<<<<<<< Updated upstream
from django.urls import path

urlpatterns = [
=======
<<<<<<< HEAD
from django.urls import path, include

from users import views as user_views
from subreddits import views as subreddit_views

from django.urls import path
from django.urls.conf import include


urlpatterns = [
    path('logout/', user_views.logout_view, name='logout'),
    path('login/', user_views.CreateLoginview.as_view(), name='login'),
    path('signup/', user_views.CreateUserView.as_view(), name='signup'),
    path('subreddit/<int:id>/', subreddit_views.subreddit_view, name='subreddit'),
    path('', include('homepage.urls')),
    path('', include('users.urls')),
    path('', include('subreddits.urls')),
>>>>>>> Stashed changes
    path('admin/', admin.site.urls),
]
