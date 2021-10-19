from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Count

from subreddits.models import Subreddit
from posts.models import Post
from spotify.views import get_recently_played
from users.models import User

@login_required
def homepage(request):
    popular_subreddits = Subreddit.objects.annotate(total_members=Count('members')).order_by('-total_members')
    posts = Post.objects.filter(is_comment=False)
    recently_played = get_recently_played(request.user.access_token)
    if 'error' in recently_played:
        if recently_played['error']['message'] == 'The access token expired':
            return redirect('/refresh_token')
        elif recently_played['error']['message'] == 'Invalid access token':
            recently_played = {}
    context = {'posts': posts, 'recently_played': recently_played, 'popular_subreddits': popular_subreddits}
    response = render(request, 'homepage.html', context)
    response.set_cookie('theme_choice', request.user.theme_choice)
    return response


def user_detail_view(request, id):
    if not User.objects.filter(id=id).exists():
        return render(request, '404.html', { "type": "User", "error": f"There is no user with id #{id}." })
    user = User.objects.get(id=id)
    subreddits = Subreddit.objects.filter(members=user)
    posts = Post.objects.filter(author=user, is_comment=False)
    comments = Post.objects.filter(author=user, is_comment=True)
    context = {'user': user, 'subreddits': subreddits, 'posts': posts, 'comments': comments}
    return render(request, 'user_detail_view.html', context)
