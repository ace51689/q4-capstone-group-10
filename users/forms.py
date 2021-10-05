from django import forms
from .models import Posts
from mptt.forms import TreeNodeChoiceField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreatePostsForm(forms.Form):
    name = forms.CharField(max_length=100)
    parent = TreeNodeChoiceField(queryset=Posts.objects.all())


class LoginForm(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
