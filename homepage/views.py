from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.db.models import Count

from subreddits.models import Subreddit
from posts.models import Post
from spotify.views import get_recently_played
from users.models import User
from users.forms import UserSettingsForm

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


def user_settings_view(request, id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        form = UserSettingsForm(request.POST)
        pass_change = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user.theme_choice = data['theme_choice']
            user.save()
            return redirect(f'/profile/{user.id}')
        if pass_change.is_valid():
            saved_user = pass_change.save()
            update_session_auth_hash(request, saved_user)
            return redirect('/')
    form = UserSettingsForm(instance=user)
    pass_change = PasswordChangeForm(user)
    context = {'form': form, 'pass_change': pass_change}
    return render(request, 'user_settings_view.html', context)
