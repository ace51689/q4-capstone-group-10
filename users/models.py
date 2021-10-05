from django.db import models
from django.contrib.auth.models import AbstractUser
from subreddits.models import Subreddit


class User(AbstractUser):
	subreddits = models.ManyToManyField(
		'subreddits.Subreddit', symmetrical=False, blank=True, related_name='users_subreddits'
	)
	access_token = models.TextField()
	refresh_token = models.TextField()
