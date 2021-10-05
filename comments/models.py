from django.db import models


class Comment(models.Model):
	body = models.TextField()
	up_votes = models.ManyToManyField('users.User', symmetrical=False, blank=True, related_name='comment_up_votes')
	down_votes = models.ManyToManyField('users.User', symmetrical=False, blank=True, related_name='comment_down_votes')
	parent_post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)

	def __str__(self):
		return self.body
