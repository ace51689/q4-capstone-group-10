from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User
from users.forms import CreateUserForm

class RedditUserAdmin(UserAdmin):
  model = User
  add_form = CreateUserForm

admin.site.register(User, RedditUserAdmin)
