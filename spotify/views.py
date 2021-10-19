from django.shortcuts import render, redirect
from django.http.response import JsonResponse
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
			request.user.refresh_token = token_response.json()['refresh_token']
			request.user.save()
			return redirect(page_redirect)


def refresh_token(request):
	token_response = requests.post(
		'https://accounts.spotify.com/api/token', headers=spot_auth_basic(),
		data={'grant_type': 'refresh_token', 'refresh_token': request.user.refresh_token}
	)
	if token_response.status_code != 400:
		request.user.access_token = token_response.json()['access_token']
		request.user.save()
		return redirect('/')
	else:
		return JsonResponse(token_response.json(), status=token_response.status_code)


def get_recently_played(access_token):
	data = requests.get(f'https://api.spotify.com/v1/me/player/recently-played/?access_token={access_token}')
	return data.json()


def play_song(request, uri):
	request.user.last_played_song = f"https://open.spotify.com/embed/{'/'.join(uri.split(':')[1:])}"
	request.user.save()
	return redirect(request.META['HTTP_REFERER'])


def share_song(request, uri):
	subreddits = request.user.subreddits.all()
	context = {'subreddits': subreddits, 'uri': uri}
	return render(request, 'browse_subreddits.html', context)


def search_song(request):
	query = request.GET.get('query')
	results = {'tracks': {'items': []}}
	if query:
		results = requests.get(f'https://api.spotify.com/v1/search/?q={query}&type=track&access_token={request.user.access_token}').json()
	return render(request, 'song_search.html', {'results': results['tracks']['items']})
