# -*- coding: utf-8 -*-

import requests
from urllib import urlencode


"""
Deezer Python Client

Resources:
http://developers.deezer.com/api

TODO:
    * Error handling
    * Tokens refreshing
"""


class DeezerClient(object):
    def __init__(self, application_key, secret_key, base_url, base_auth_url, redirect_uri, perms=None):
        # required at init
        self.application_key = application_key
        self.secret_key = secret_key
        self.base_url = base_url
        self.base_auth_url = base_auth_url
        self.redirect_uri = redirect_uri
        self.perms = perms

        # not required
        self.access_token = None


    def _make_request(self, method, base_url, endpoint, params={}):
        params['request_method'] = method
        if base_url == self.base_url:
            params['access_token'] = self.access_token
        url = base_url + "/%s" % endpoint
        result = requests.get(url, params=params)
        return result

    """Auth flow
       http://developers.deezer.com/api/oauth
    """
    def get_auth_url(self):
        params = {}
        params['app_id'] = self.application_key
        params['redirect_uri'] = self.redirect_uri
        params['perms'] = self.perms
        endpoint = '/auth.php'
        return self.base_auth_url + "%s?%s" % (endpoint, urlencode(params))

    def get_auth_token(self, code):
        params = {}
        params['app_id'] = self.application_key
        params['secret'] = self.secret_key
        params['code'] = code
        result = self._make_request(
            method='GET',
            base_url=self.base_auth_url,
            endpoint='/access_token.php',
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

    def me(self):
        result = self._make_request(
            method='GET',
            base_url=self.base_url,
            endpoint='/user/me',
        )
        return result

    def search_track(self, query, params={}):
        """http://developers.deezer.com/api/search/track
        """
        params['q'] = query
        result = self._make_request(
            method='GET',
            base_url=self.base_url,
            endpoint='/search/track',
            params=params,
        )
        result = result and result.json()
        if not result:
            return
        return result

    def get_track(self, query, params={}):
        """http://developers.deezer.com/api/track/
        """
        result = self._make_request(
            method='GET',
            base_url=self.base_url,
            endpoint="/track/%s" % query,
        )
        result = result and result.json()
        if not result:
            return
        return result

    def playlist_create(self, title):
        """http://developers.deezer.com/api/playlist#actions
        """
        params = {}
        params['title'] = title
        result = self._make_request(
            method='POST',
            base_url=self.base_url,
            endpoint='/user/me/playlists',
            params=params,
        )
        return result

    def playlist_info(self, playlist_id):
        params = {}
        endpoint = '/playlist/%s' % playlist_id
        result = self._make_request(
            method='GET',
            base_url=self.base_url,
            endpoint=endpoint,
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
            base_url=self.base_url,
            endpoint=endpoint,
            params=params,
        )
        return result

    def playlist_remove_tracks(self, playlist_id, track_ids):
        """http://developers.deezer.com/api/track#actions
        """
        params = {}
        track_ids = ",".join([str(track_id) for track_id in track_ids])
        params['songs'] = track_ids
        endpoint = '/playlist/%s/tracks' % playlist_id
        result = self._make_request(
            method='DELETE',
            base_url=self.base_url,
            endpoint=endpoint,
            params=params,
        )
        return result

    def user_history(self):
        result = self._make_request(
            method='GET',
            base_url=self.base_url,
            endpoint='/user/me/history',
            params={}
        )
        result = result.json()
        return result
