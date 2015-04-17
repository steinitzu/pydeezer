"""
Deezer Python Client

Resources:
http://developers.deezer.com/api

TODO: 
	* Error handling
	* Tokens refreshing
"""

import requests
from urllib import urlencode


BASE_URL = "https://api.deezer.com"
BASE_AUTH_URL = "https://connect.deezer.com/oauth"
REDIRECT_URI = "http://localhost:8000/services/deezer/auth"


class DeezerClient(object):
	def __init__(self, application_key, secret_key):
		self.application_key = application_key
		self.secret_key = secret_key
		self.access_token = None

	def _make_request(self, method, base_url, endpoint, params):
		params['request_method'] = method
		if base_url == BASE_URL:
			params['access_token'] = self.access_token
		url = base_url + "%s?%s" % (endpoint, urlencode(params))
		logger.info("Making request to %s", url)
		result = requests.get(url, params=params)
		return result

	"""Auth flow
	   http://developers.deezer.com/api/oauth
	"""
	def get_auth_url(self):
		params = {}
		params['app_id'] = self.application_key
		params['redirect_uri'] = REDIRECT_URI
		params['perms'] = "manage_library"
		endpoint = '/auth'
		return BASE_AUTH_URL + "%s?%s" % (endpoint, urlencode(params))

	def get_auth_token(self, code):
		params = {}
		params['app_id'] = self.application_key
		params['secret'] = self.secret_key
		params['code'] = code
		result = self._make_request(
			method='GET',
			base_url=BASE_AUTH_URL,
			endpoint='/access_token',
			params=params
		)
		auth_token_string = result.text
		auth_token = self._parse_auth_token(auth_token_string)
		return auth_token

	def refresh_token(self):
		pass

	def _parse_auth_token(self, auth_token_string):
		params = auth_token_string.split('&')
		result = {}
		for param in params:
			key, value = param.split('=')
			result[key] = value
		return result

	"""api endpoints"""
	def search_track(self, query):
		"""http://developers.deezer.com/api/search/track
		"""
		params = {}
		params['q'] = query
		result = self._make_request(
			method='GET',
			base_url=BASE_URL,
			endpoint='/search/track',
			params=params,
		)
		return result

	def playlist_create(self, title):
		"""http://developers.deezer.com/api/playlist#actions
		"""
		params = {}
		params['title'] = title
		result = self._make_request(
			method='POST',
			base_url=BASE_URL,
			endpoint='/user/me/playlists',
			params=params,
		)
		return result

	def playlist_add_tracks(self, playlist_id, track_ids):
		"""http://developers.deezer.com/api/track#actions
		"""
		params = {}
		track_ids = ",".join([str(track_id) for track_id in track_ids])
		params['songs'] = track_ids
		endpoint = '/playlist/%s/tracks' % playlist_id
		result = self._make_request(
			method='POST',
			base_url=BASE_URL,
			endpoint=endpoint,
			params=params,
		)
		return result
