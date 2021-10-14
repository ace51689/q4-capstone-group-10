from django import forms
from django.forms.widgets import Textarea

class CreatePostForm(forms.Form):
  title = forms.CharField(max_length=100)
  body = forms.CharField(widget=Textarea)

class CreateCommentForm(forms.Form):
  body = forms.CharField(widget=Textarea)