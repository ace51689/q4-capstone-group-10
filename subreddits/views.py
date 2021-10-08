from django.shortcuts import render, reverse, HttpResponseRedirect
from django.views.generic import View
from subreddits.forms import CreateSubredditForm, EditSubredditForm
from subreddits.models import Subreddit
from posts.models import Post

# Create your views here.
def subreddit_view(request, id):
  subreddit = Subreddit.objects.get(id=id)
  posts = Post.objects.filter(subreddit=id)
  return render(request, 'subreddit.html', { 'subreddit': subreddit, 'posts': posts })

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
      
      return render(request, self.template_name, { 'form': self.form})

    return render(request, self.template_name, { "form": self.form })


def edit_subreddit_view(request, id):
  subreddit = Subreddit.objects.get(id=id)

  if request.method == "POST":
    form = EditSubredditForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      subreddit.moderators.add(data.get('moderators')[0])
      return HttpResponseRedirect(reverse("subreddit", args=(id,)))

  form = EditSubredditForm()

  return render(request, "signup.html", { "form": form })

