from django.shortcuts import render
from posts.models import Post

# Create your views here.

def homepage(request):
    context = {'posts': Post.objects.filter(is_comment=False)}
    return render(request, 'homepage.html', context)
