from django.shortcuts import render
from .models import Post
from .forms import PostCreationForm
from . import PostsSerializer
from rest_framework import generics, permissions
# Create your views here.


class post_creation_view(generics.ListCreatePIView)
queryset = Post.objects.all()
serializer_class = PostsSerializer
permission_classes = {permissions.IsAuthenticatedOrReadOnly}

def perform_create(self, serializer)
serializer.save(poster=self.request.user.)
