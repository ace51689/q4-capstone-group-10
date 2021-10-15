from django.shortcuts import render, reverse, HttpResponseRedirect
from django.views.generic import View
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from subreddits.forms import CreateSubredditForm, AddModeratorForm, RemoveModChangeAdminForm, DeleteSubredditForm
from subreddits.models import Subreddit
from posts.models import Post

# Create your views here.
def subreddit_view(request, id):
  subreddit = Subreddit.objects.get(id=id)
  posts = Post.objects.filter(subreddit=id)
  members = subreddit.members.all()
  context = { 'subreddit': subreddit, 'posts': posts, 'members': members }
  return render(request, 'subreddit.html', context)

class CreateSubredditView(LoginRequiredMixin, View):
  template_name = 'signup.html'
  form = CreateSubredditForm()

  def get(self, request):
    return render(request, self.template_name, { 'form': self.form })

  def post(self, request):
    form = CreateSubredditForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      subreddit = Subreddit(
        name=data.get('name'),
        admin=request.user
      )
      subreddit.save()
      subreddit.members.add(request.user)
      return HttpResponseRedirect(reverse('subreddit', args=(subreddit.id,)))
      
    return render(request, self.template_name, { 'form': self.form })


@login_required
def add_moderator_view(request, id):
  subreddit = Subreddit.objects.get(id=id)

  if request.method == "POST":
    form = AddModeratorForm(subreddit, request.POST)
    if form.is_valid():
      data = form.cleaned_data
      moderator_to_add = data.get('moderators')[0]
      subreddit.moderators.add(moderator_to_add)
      return HttpResponseRedirect(reverse("subreddit", args=(id,)))

  form = AddModeratorForm(subreddit)

  return render(request, "signup.html", { "form": form })


@login_required
def remove_moderator_view(request, id):
  subreddit = Subreddit.objects.get(id=id)

  if request.method == "POST":
    form = RemoveModChangeAdminForm(subreddit, request.POST)
    if form.is_valid():
      data = form.cleaned_data
      moderator_to_remove = data.get('moderators')[0]
      subreddit.moderators.remove(moderator_to_remove)
      return HttpResponseRedirect(reverse("subreddit", args=(id,)))

  form = RemoveModChangeAdminForm(subreddit)

  return render(request, "signup.html", { "form": form })


@login_required
def change_admin_view(request, id):
  subreddit = Subreddit.objects.get(id=id)

  if request.method == "POST":
    form = RemoveModChangeAdminForm(subreddit, request.POST)
    if form.is_valid():
      data = form.cleaned_data
      moderator_to_promote = data.get('moderators')[0]
      subreddit.admin = moderator_to_promote
      subreddit.moderators.remove(moderator_to_promote)
      subreddit.save()
      return HttpResponseRedirect(reverse("subreddit", args=(id,)))

  form = RemoveModChangeAdminForm(subreddit)

  return render(request, "signup.html", { "form": form })


@login_required
def join_subreddit(request, id):
  subreddit_to_join = Subreddit.objects.get(id=id)
  subreddit_to_join.members.add(request.user)
  request.user.subreddits.add(subreddit_to_join)
  return HttpResponseRedirect(reverse('subreddit', args=(id,)))


@login_required
def leave_subreddit(request, id):
  subreddit_to_leave = Subreddit.objects.get(id=id)
  subreddit_to_leave.members.remove(request.user)
  request.user.subreddits.remove(subreddit_to_leave)
  return HttpResponseRedirect(reverse('subreddit', args=(id,)))


@login_required
def delete_subreddit_view(request, id):
  
  if request.method == "POST":
    form = DeleteSubredditForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      subreddit_to_delete = Subreddit.objects.get(id=id)
      admin = subreddit_to_delete.admin
      if admin.check_password(data.get('password')):
        subreddit_to_delete.delete()
        return HttpResponseRedirect(reverse('homepage'))
      
      return HttpResponseRedirect(reverse("subreddit", args=(id,)))

  form = DeleteSubredditForm()

  return render(request, "delete_subreddit.html", { "form": form })


def browse_subreddits_view(request):
  context = { 'subreddits': Subreddit.objects.annotate(
              post_count=Count('posts')).order_by('-post_count') }
  
  return render(request, 'browse_subreddits.html', context)