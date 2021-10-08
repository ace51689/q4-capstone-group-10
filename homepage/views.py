from django.shortcuts import render
from posts.models import Post

# Create your views here.

def homepage(request):
    context = {'posts': Post.objects.all()}
    return render(request, 'homepage.html', context)
