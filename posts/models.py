from django.db import models


class Post(models.Model):
	title = models.CharField(max_length=100)
	body = models.TextField()
	author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='user')
	up_votes = models.ManyToManyField('users.User', symmetrical=False, blank=True, related_name='post_up_votes')
	down_votes = models.ManyToManyField('users.User', symmetrical=False, blank=True, related_name='post_down_votes')
	subreddit = models.ForeignKey('subreddits.Subreddit', on_delete=models.CASCADE)

	def __str__(self):
		return self.title
