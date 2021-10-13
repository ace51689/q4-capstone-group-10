from django.shortcuts import redirect, reverse
from string import ascii_letters, digits
from django.contrib import messages
from urllib.parse import urlencode
from environ import Env
import requests
import random
import base64

env = Env()
Env.read_env()
redirect_url = None
page_redirect = None
state_key = env('STATE_KEY')


def generate_id(length):
	return ''.join([random.choice(ascii_letters + digits) for _ in range(length)])


def spot_auth_basic():
	basic_token = base64.b64encode((env('CLIENT_ID') + ':' + env('CLIENT_SECRET')).encode('ascii')).decode('ascii')
	return {'Authorization': f"basic {basic_token}"}


def connect_spotify(request):
	global redirect_url, page_redirect
	state = generate_id(16)
	page_redirect = request.GET.get('next', '/')
	redirect_url = f"{request.META['wsgi.url_scheme']}://{request.META['HTTP_HOST']}/callback"
	url_query = {
		'client_id': env('CLIENT_ID'),
		'redirect_uri': redirect_url,
		'response_type': 'code',
		'scope': env('SCOPE'),
		'state': state,
	}
	response = redirect(f'https://accounts.spotify.com/authorize?{urlencode(url_query)}')
	response.set_cookie(state_key, state)
	return response


def callback_action(request):
	global redirect_url
	code = request.GET.get('code', '')
	state = request.GET.get('state', '')
	stored_state = request.COOKIES[state_key]
	if state is None or state != stored_state:
		messages.error(request, 'Forbidden!')
		return redirect('/')
	else:
		token_response = requests.post('https://accounts.spotify.com/api/token', data={
			'code': code,
			'redirect_uri': redirect_url,
			'grant_type': 'authorization_code'
		}, headers=spot_auth_basic())
		if token_response.status_code == 400:
			messages.error(request, f"reason: {token_response.reason}, {token_response.text}")
			return redirect(page_redirect)
		else:
			request.user.access_token = token_response.json()['access_token']
			request.user.save()
			return redirect(page_redirect)
