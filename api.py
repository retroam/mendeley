"""

"""

import os
import json
import base64
import urllib
import datetime

import requests
from requests_oauthlib import OAuth2Session
from hurry.filesize import size, alternative

from . import settings as mendeley_settings

GH_URL = 'https://mendeley.com/'
API_URL = 'https://api-oauth2.mendeley.com/oapi/'


mendeley_cache = {}


class Mendeley(object):

    def __init__(self, access_token=None, token_type=None):

        self.access_token = access_token
        self.token_type = token_type

        if access_token and token_type:
            self.session = OAuth2Session(
                mendeley_settings.CLIENT_ID,
                token={
                    'access_token': access_token,
                    'token_type': token_type,
                }
            )
        else:
            self.session = requests

    @classmethod
    def from_settings(cls, settings):
        if settings:
            return cls(
                access_token=settings.oauth_access_token,
                token_type=settings.oauth_token_type,
            )
        return cls()

    def _send(self, url, method='get', output='json', cache=True, **kwargs):
        """

        """
        func = getattr(self.session, method.lower())

        # Add if-modified-since header if needed
        headers = kwargs.pop('headers', {})
        cache_key = '{0}::{1}::{2}'.format(
            url, method, str(kwargs)
        )
        cache_data = mendeley_cache.get(cache_key)
        if cache and cache_data:
            if 'if-modified-since' not in headers:
                headers['if-modified-since'] = cache_data['date'].strftime('%c')

        # Send request
        req = func(url, headers=headers, **kwargs)

        # Pull from cache if not modified
        if cache and cache_data and req.status_code == 304:
            return cache_data['data']

        # Get return value

        if 200 <= req.status_code < 300:
            if output is None:
                rv = req
            else:
                rv = getattr(req, output)
                if callable(rv):
                    rv = rv()

        # Cache return value if needed
        if cache and rv:
            if req.headers.get('last-modified'):
                mendeley_cache[cache_key] = {
                    'data': rv,
                    'date': datetime.datetime.utcnow(),
                }

        return rv

    def user(self, user=None):
        """Fetch a user or the authenticated user.

        :param user: Optional Mendeley user name; will fetch authenticated
            user if omitted
        :return dict: Mendeley API response

        """
        url = (
            os.path.join(API_URL, 'users', user)
            if user
            else os.path.join(API_URL, 'profiles','info','me')
        )

        return self._send(url, cache=False)

    def revoke_token(self):

        if self.access_token is None:
            return

        return self._send(
            os.path.join(
                API_URL, 'applications', mendeley_settings.CLIENT_ID,
                'tokens', self.access_token,
            ),
            method='delete',
            cache=False,
            output=None,
            auth=(
                mendeley_settings.CLIENT_ID,
                mendeley_settings.CLIENT_SECRET,
            )
        )



    def library(self, user):
        """Get library from user collection
        """
        return self._send(
            os.path.join(API_URL, 'library')
        )

    def folders(self, user):
        """Get folders from user collection
        """
        return self._send(
            os.path.join(API_URL, 'library', 'folders')
        )

    def folder_details(self, user, folder_id):
        """Get folders from user collection
        """
        return self._send(
            os.path.join(API_URL, 'library', 'folders', folder_id)
        )

    def document_details(self, user,doc_id):
        """Get document details from user collection
        """
        return self._send(
            os.path.join(API_URL, 'library', 'documents' , doc_id)
        )


def raw_url(user, repo, ref, path):
    return os.path.join(
        GH_URL, user, repo, 'blob', ref, path
    ) + '?raw=true'


type_map = {
    'tree': 'folder',
    'blob': 'file',
    'file': 'file',
    'dir': 'folder'
}


