from posts.models import Post
<<<<<<< Updated upstream
from django.contrib.auth import models
=======
>>>>>>> Stashed changes
from django import forms


class PostCreationForm(forms.ModelForm):
    class Meta:

        model = Post
        fields = ('title', 'body')
