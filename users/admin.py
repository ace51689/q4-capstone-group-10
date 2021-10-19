from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User
from users.forms import CreateUserForm


class RedditUserAdmin(UserAdmin):
	model = User
	add_form = CreateUserForm
	list_display = ['username', 'is_staff', 'is_premium']
	UserAdmin.fieldsets[0][1]['fields'] += (
		'access_token', 'refresh_token', 'is_premium',
		'last_played_song', 'theme_choice'
	)


admin.site.register(User, RedditUserAdmin)
