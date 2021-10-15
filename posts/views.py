from django.shortcuts import render, HttpResponseRedirect, reverse
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
      subreddit.posts.add(post)
      return HttpResponseRedirect(reverse('post', args=(post.id,)))

  form = CreatePostForm()

  return render(request, 'create_post.html', { 'form': form })


def create_comment_view(request, id):
  post = Post.objects.get(id=id)

  if request.method == 'POST':
    form = CreateCommentForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      comment = Post(
        body = data.get('body'),
        is_comment = True,
        author = request.user,
        parent = post
      )
      comment.save()
      return HttpResponseRedirect(reverse('post', args=(post.id,)))

  form = CreateCommentForm()

  return render(request, 'create_post.html', { 'form': form })

# TODO: Add login_required decorator. Stretch: Display conformation or 'are you sure?' message
def delete_post_view(request, id):
  post_to_delete = Post.objects.get(id=id)
  author = post_to_delete.author
  # print(author)
  subreddit_moderators = post_to_delete.subreddit.moderators.all()
  subreddit_admin = post_to_delete.subreddit.admin
  # print(subreddit_admin)
  user = request.user
  if user == author or user in subreddit_moderators or user == subreddit_admin:
    # post_to_delete.delete()
    print('yep')
    return HttpResponseRedirect(reverse('homepage'))
    
  return HttpResponseRedirect(reverse('post', args=(id)))
