from django.contrib.auth.forms import UserCreationForm
from users.models import User
from django import forms 

class CreateUserForm(UserCreationForm):
  class Meta:
    model = User
    fields = ('username', 'password1', 'password2',)

class LoginForm(forms.Form):
  username = forms.CharField(max_length=50)
  password = forms.CharField(widget=forms.PasswordInput)
