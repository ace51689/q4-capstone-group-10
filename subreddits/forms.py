from django import forms
from django.forms import fields
from users.models import User
from subreddits.models import Subreddit

'''
	name = models.CharField(max_length=30)
	admin = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='admin')
	members = models.ManyToManyField('users.User', symmetrical=False, blank=True, related_name='members')
	moderators = models.ManyToManyField('users.User', symmetrical=False, blank=True, related_name='moderators')
	posts = models.ManyToManyField('posts.Post', symmetrical=False, blank=True, related_name='subreddit_posts')
  '''

class CreateSubredditForm(forms.Form):
  name = forms.CharField(max_length=30)

class EditSubredditForm(forms.ModelForm):
  # moderators = forms.ModelMultipleChoiceField(queryset=User.objects.all())

  def __init__(self, subreddit, *args, **kwargs):
    super(EditSubredditForm, self).__init__(*args, **kwargs)
    self.fields['moderators'].queryset = subreddit.members.all()

  class Meta:
    model = Subreddit
    fields = ('moderators', )