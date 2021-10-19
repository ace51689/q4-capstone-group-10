from django import template

register = template.Library()


@register.filter(name='default_theme')
def default_theme(theme, cookies):
	return theme if theme else cookies['theme_choice'] if 'theme_choice' in cookies else 'theme_light.css'
