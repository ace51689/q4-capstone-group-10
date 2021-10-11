from django.shortcuts import render
from .models import Post
from .forms import PostCreationForm

# Create your views here.

def post_creation_view(request, id):
    post_creation_view = Post_Creation_View.objects.get(id=id)
    posts = Post.objects.filter(post_creation_view=id)
    return render(request, 'post_creation_form.html', { 'post_creation_view': post_creation_view, 'posts': posts })
