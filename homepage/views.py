from django.contrib.auth import get_user_model
from django.shortcuts import render
from posts.models import Post


def homepage(request):
    context = {'posts': Post.objects.all()}
    return render(request, 'homepage.html', context)


def user_detail_view(request, id):
    user = get_user_model().objects.get(id=id)
    return render(request, 'user_detail_view.html', {'user': user})
