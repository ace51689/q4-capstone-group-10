from django.shortcuts import render, HttpResponseRedirect, reverse
from django.views.generic import View
from posts.models import Post
from subreddits.models import Subreddit
from posts.forms import CreatePostForm, CreateCommentForm

# Create your views here.
def post_view(request, id):
  post = Post.objects.get(id=id)
  return render(request, 'post.html', { 'post': post })


def create_post_view(request, id):
  subreddit = Subreddit.objects.get(id=id)

  if request.method == 'POST':
    form = CreatePostForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      post = Post(
        title = data.get('title'),
        body = data.get('body'),
        is_comment = False,
        author = request.user,
        subreddit = subreddit,
      )
      post.save()
      return HttpResponseRedirect(reverse('post', args=(post.id,)))

  form = CreatePostForm()

  return render(request, 'create_post.html', { 'form': form })
