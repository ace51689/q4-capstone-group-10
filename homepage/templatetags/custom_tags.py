from django import template
import re

register = template.Library()


@register.filter(name='default_theme')
def default_theme(theme, cookies):
	return theme if theme else cookies['theme_choice'] if 'theme_choice' in cookies else 'theme_light.css'


@register.filter(name='uri_to_link')
def uri_to_link(uri):
	return f"https://open.spotify.com/embed/{'/'.join(uri.split(':')[1:])}"


@register.filter(name='retrieve_link')
def retrieve_link(text):
	return re.findall('(\w*:\w*:\w*)', text)[0]