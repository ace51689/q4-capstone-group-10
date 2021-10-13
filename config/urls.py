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
<<<<<<< HEAD
from django.urls import path, include

from users import views as user_views
from subreddits import views as subreddit_views
=======
from django.urls import path
from django.urls.conf import include
>>>>>>> cf3a4cb13565d7b72f94ca0e43e97cc5f3b6f2ad


urlpatterns = [
<<<<<<< HEAD
    path('logout/', user_views.logout_view, name='logout'),
    path('login/', user_views.CreateLoginview.as_view(), name='login'),
    path('signup/', user_views.CreateUserView.as_view(), name='signup'),
    path('subreddit/<int:id>/', subreddit_views.subreddit_view, name='subreddit'),
    path('postcreation/<int:id>/', posts_views.post_creation_view.as_view(), name='postcreation'),
    path('Posts/', include('Posts.urls')),
=======
    path('', include('homepage.urls')),
    path('', include('users.urls')),
    path('', include('subreddits.urls')),
<<<<<<< HEAD
>>>>>>> cf3a4cb13565d7b72f94ca0e43e97cc5f3b6f2ad
=======
    path('', include('spotify.urls')),
>>>>>>> 0fbc9f1571f729e2ff27bcbb898f09835d244557
    path('admin/', admin.site.urls),
]
