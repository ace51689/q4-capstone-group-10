from django.contrib.auth import get_user_model
from subreddits.models import Subreddit
from django.shortcuts import render
from posts.models import Post


def homepage(request):
    context = {'posts': Post.objects.filter(is_comment=False)}
    return render(request, 'homepage.html', context)


def user_detail_view(request, id):
    user = get_user_model().objects.get(id=id)
    subreddits = Subreddit.objects.filter(members=user)
    posts = Post.objects.filter(author=user, is_comment=False)
    comments = Post.objects.filter(author=user, is_comment=True)
    context = {'user': user, 'subreddits': subreddits, 'posts': posts, 'comments': comments}
    return render(request, 'user_detail_view.html', context)
