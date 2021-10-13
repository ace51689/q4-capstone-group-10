from django.shortcuts import render
from .models import Post
from .forms import PostCreationForm


# Create your views here.

def post_view(request, id):
    post=Post.objects.get(id=id)
    return render(request, 'post.html', {'post': post})



