from django.db import models
from django.contrib.auth.models import AbstractUser
from subreddits.models import Subreddit


class User(AbstractUser):
	subreddits = models.ManyToManyField(
		'subreddits.Subreddit', symmetrical=False, blank=True, related_name='users_subreddits'
	)
	access_token = models.TextField(null=True, blank=True)
	refresh_token = models.TextField(null=True, blank=True)
	is_premium = models.BooleanField(default=False)
	last_played_song = models.URLField(null=True, blank=True)
	theme_choice = models.CharField(
		max_length=15, default='theme_three.css',
		choices=[
			('theme_one.css', 'One'),
			('theme_two.css', 'Two'),
			('theme_three.css', 'Three'),
			('theme_four.css', 'Four'),
			('theme_light.css', 'Light'),
			('theme_dark.css', 'Dark'),
		])
