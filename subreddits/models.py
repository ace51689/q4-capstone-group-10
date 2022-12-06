from django.db import models


class Subreddit(models.Model):
	name = models.CharField(max_length=30) #TODO: Add unique=True to name field
	#TODO: Add a title field that is editable by the admin of the subreddit
	#TODO: Add a description TextField so users can know what this sub is all about
	admin = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='admin')
	members = models.ManyToManyField('users.User', symmetrical=False, blank=True, related_name='members')
	moderators = models.ManyToManyField('users.User', symmetrical=False, blank=True, related_name='moderators')

	def __str__(self):
		return self.name
