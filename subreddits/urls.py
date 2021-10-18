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
from django.urls import path, include
from subreddits import views

urlpatterns = [
    path('subreddit/<int:id>/', views.subreddit_view, name='subreddit'),
    path('subreddit/create/', views.CreateSubredditView.as_view(), name='create-subreddit'),
    path('subreddit/<int:id>/add-moderator/', views.add_moderator_view, name='add-moderator'),
    path('subreddit/<int:id>/remove-moderator/', views.remove_moderator_view, name='remove-moderator'),
    path('subreddit/<int:id>/change-admin/', views.change_admin_view, name='change-admin'),
    path('subreddit/<int:id>/join/', views.join_subreddit, name='join-subreddit'),
    path('subreddit/<int:id>/leave/', views.leave_subreddit, name='leave-subreddit'),
    path('subreddit/browse/', views.browse_subreddits_view, name='browse-subreddits'),
    path('subreddit/<int:id>/delete/', views.delete_subreddit_view, name='delete-subreddit'),
]
