from django import forms
from django.forms.widgets import TextInput, Textarea

class CreatePostForm(forms.Form):
  title = forms.CharField(max_length=100)
  body = forms.CharField(widget=TextInput)

class CreateCommentForm(forms.Form):
  body = forms.CharField(widget=Textarea)