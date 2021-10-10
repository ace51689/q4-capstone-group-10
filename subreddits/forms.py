from django import forms
from django.forms import fields
from django.forms.widgets import PasswordInput
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

class AddModeratorForm(forms.ModelForm):

  def __init__(self, subreddit, *args, **kwargs):
    super(AddModeratorForm, self).__init__(*args, **kwargs)
    member_ids = [member.id for member in subreddit.members.all()]
    admin_id = subreddit.admin.id
    moderator_ids = [moderator.id for moderator in subreddit.moderators.all()]
    member_ids.remove(admin_id)
    for moderator_id in moderator_ids:
      member_ids.remove(moderator_id)
    potential_moderators = subreddit.members.filter(id__in=member_ids)
    self.fields['moderators'].queryset = potential_moderators

  class Meta:
    model = Subreddit
    fields = ('moderators', )


class RemoveModChangeAdminForm(forms.ModelForm):

  def __init__(self, subreddit, *args, **kwargs):
    super(RemoveModChangeAdminForm, self).__init__(*args, **kwargs)
    moderators = subreddit.moderators.all()
    self.fields['moderators'].queryset = moderators

  class Meta:
    model = Subreddit
    fields = ('moderators', )


class DeleteSubredditForm(forms.Form):
  password = forms.CharField(max_length=128, widget=PasswordInput)