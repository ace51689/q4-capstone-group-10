from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required

from posts.models import Post
from subreddits.models import Subreddit
from posts.forms import CreatePostForm, CreateCommentForm

# Create your views here.
def post_view(request, id):
    if not Post.objects.filter(id=id).exists():
      return render(request, '404.html', { "type": "Post", "error": f"There is no post with id #{id}." })
    post = Post.objects.get(id=id)
    return render(request, 'post.html', { 'post': post })

@login_required
def create_post_view(request, id):
  if not Subreddit.objects.filter(id=id).exists():
    return render(request, '404.html', { "type": "Subreddit", "error": f"There is no subreddit with id #{id}." })
  
  subreddit = Subreddit.objects.get(id=id)

  if request.method == 'POST':
    form = CreatePostForm(request.POST)

    if request.user not in subreddit.members.all():
      e = f"Logged in user not a member of r/{subreddit.name}."
      return render(request, 'create_post.html', { 'form': CreatePostForm(), 'subreddit': subreddit, "error": e })
    
    elif form.is_valid():
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

  return render(request, 'create_post.html', { 'form': form, 'subreddit': subreddit })

@login_required
def create_comment_view(request, id):
  if not Post.objects.filter(id=id).exists():
      return render(request, '404.html', { "type": "Post", "error": f"There is no post with id #{id}." })
  post = Post.objects.get(id=id)
  subreddit = post.subreddit
  root_post = post.get_root()

  if request.method == 'POST':
    form = CreateCommentForm(request.POST)
    
    if request.user not in subreddit.members.all():
      e = f"Logged in user not a member of r/{subreddit.name}."
      return render(request, 'create_comment.html', { 'form': CreateCommentForm(), 'post': post, 'subreddit': subreddit, "root_post": root_post, "error": e })
    
    if form.is_valid():
      data = form.cleaned_data
      comment = Post(
        body = data.get('body'),
        is_comment = True,
        author = request.user,
        subreddit = subreddit,
        parent = post
      )
      comment.save()
      return HttpResponseRedirect(reverse('post', args=([post.get_root().id])))

  form = CreateCommentForm()

  return render(request, 'create_comment.html', { 'form': form, "subreddit": subreddit, 'post': post, "root_post": root_post })

# TODO: Stretch: Display conformation or 'are you sure?' message
@login_required
def delete_post_view(request, id):
  if not Post.objects.filter(id=id).exists():
      return render(request, '404.html', { "type": "Post", "error": f"There is no post with id #{id}." })
  post_to_delete = Post.objects.get(id=id)
  author = post_to_delete.author
  subreddit_moderators = post_to_delete.subreddit.moderators.all()
  subreddit_admin = post_to_delete.subreddit.admin
  user = request.user
  if user == author or user in subreddit_moderators or user == subreddit_admin:
    if post_to_delete.is_comment:
      post_to_delete.delete()
      return HttpResponseRedirect(reverse('post', args=([post_to_delete.get_root().id])))
    
    post_to_delete.delete()
    return HttpResponseRedirect(reverse('subreddit', args=(post_to_delete.subreddit.id,)))
 
  e = "You do not have privileges to delete this post."
  return render(request, 'post.html', { "post": post_to_delete, "error": e })


@login_required
def upvote_post(request, id):
  if not Post.objects.filter(id=id).exists():
      return render(request, '404.html', { "type": "Post", "error": f"There is no post with id #{id}." })
  post = Post.objects.get(id=id)
  if request.user in post.up_votes.all():
    post.up_votes.remove(request.user)
  elif request.user in post.down_votes.all():
    post.down_votes.remove(request.user)
    post.up_votes.add(request.user)
  else:
    post.up_votes.add(request.user)
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def downvote_post(request, id):
  if not Post.objects.filter(id=id).exists():
      return render(request, '404.html', { "type": "Post", "error": f"There is no post with id #{id}." })
  post = Post.objects.get(id=id)
  if request.user in post.down_votes.all():
    post.down_votes.remove(request.user)
  elif request.user in post.up_votes.all():
    post.up_votes.remove(request.user)
    post.down_votes.add(request.user)
  else:
    post.down_votes.add(request.user)
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
