from django.shortcuts import render
from subreddits.models import Subreddit
from posts.models import Post

# Create your views here.
def subreddit_view(request, id):
  subreddit = Subreddit.objects.get(id=id)
  posts = Post.objects.filter(subreddit=id)
  return render(request, 'subreddit.html', { 'subreddit': subreddit, 'posts': posts })
