from django.shortcuts import render, reverse, HttpResponseRedirect
from django.views.generic import View
from subreddits.forms import CreateSubredditForm, EditSubredditForm
from subreddits.models import Subreddit
from posts.models import Post

# Create your views here.
def subreddit_view(request, id):
  subreddit = Subreddit.objects.get(id=id)
  posts = Post.objects.filter(subreddit=id)
  members = subreddit.members.all()
  context = { 'subreddit': subreddit, 'posts': posts, 'members': members }
  return render(request, 'subreddit.html', context)

class CreateSubredditView(View):
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


def edit_subreddit_view(request, id):
  subreddit = Subreddit.objects.get(id=id)

  if request.method == "POST":
    form = EditSubredditForm(subreddit, request.POST)
    if form.is_valid():
      data = form.cleaned_data
      moderator_to_add = data.get('moderators')[0]
      subreddit.moderators.add(moderator_to_add)
      return HttpResponseRedirect(reverse("subreddit", args=(id,)))

  form = EditSubredditForm(subreddit)

  return render(request, "signup.html", { "form": form })


def join_subreddit(request, id):
  subreddit_to_join = Subreddit.objects.get(id=id)
  subreddit_to_join.members.add(request.user)
  request.user.subreddits.add(subreddit_to_join)
  return HttpResponseRedirect(reverse('subreddit', args=(id,)))


def leave_subreddit(request, id):
  subreddit_to_leave = Subreddit.objects.get(id=id)
  subreddit_to_leave.members.remove(request.user)
  request.user.subreddits.remove(subreddit_to_leave)
  return HttpResponseRedirect(reverse('subreddit', args=(id,)))

