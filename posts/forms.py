from posts.models import Post
from django.contrib.auth import ModelForm


class PostCreationForm(forms.ModelForm):
    class Meta:

        model = Post
        fields = ('Title', 'Create Post')