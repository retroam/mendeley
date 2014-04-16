"""
Get access to Mendeley using OAuth 2.0.
"""

import os
from requests_oauthlib import OAuth2Session

from website import settings
from . import settings as mendeley_settings

OAUTH_AUTHORIZE_URL = 'https://api-oauth2.mendeley.com/oauth/authorize'
OAUTH_ACCESS_TOKEN_URL = 'https://api-oauth2.mendeley.com/oauth/token'


def oauth_start_url(user, node=None):
    """Get authorization URL for OAuth.

    :param User user: OSF user
    :param Node node: OSF node
    :return tuple: Tuple of authorization URL and OAuth state

    """

    uri_parts = [
        settings.DOMAIN, 'api', 'v1', 'addons', 'mendeley',
        'callback', user._id,
    ]
    if node:
        uri_parts.append(node._id)
   # redirect_uri = 'http://0.0.0.0:5000/api/v1/addons/mendeley/callback/%s/' % user._id
    redirect_uri = 'http://0.0.0.0:5000/api/v1/addons/mendeley/callback/j2isr'



    session = OAuth2Session(
        mendeley_settings.CLIENT_ID,
        redirect_uri=redirect_uri,
        scope=mendeley_settings.SCOPE,
    )
    return session.authorization_url(OAUTH_AUTHORIZE_URL)

##TODO pass parameters into token

def oauth_get_token(code,user):
    """Get OAuth access token.

    :param str code: Authorization code from provider
    :return str: OAuth access token

    """
    redirect_uri = 'http://0.0.0.0:5000/api/v1/addons/mendeley/callback/j2isr'
    session = OAuth2Session(
        mendeley_settings.CLIENT_ID,
        redirect_uri=redirect_uri
    )


    return session.fetch_token(
        OAUTH_ACCESS_TOKEN_URL,
        client_secret=mendeley_settings.CLIENT_SECRET,
        code=code,
    )


def oauth_refresh_token(code,refresh_token,user,expires_in,token):
    """Refresh OAuth access token.

    :param str code: Authorization code from provider
    :return str: OAuth access token

    """
    redirect_uri = 'http://0.0.0.0:5000/api/v1/addons/mendeley/callback/j2isr'
    #redirect_uri = 'http://0.0.0.0:5000/api/v1/addons/mendeley/callback/%s/' % user._id
    session = OAuth2Session(
        mendeley_settings.CLIENT_ID,
        redirect_uri=redirect_uri,
        token=token,
    )


    return session.refresh_token(
        OAUTH_ACCESS_TOKEN_URL,
        client_secret=mendeley_settings.CLIENT_SECRET,
        client_id=mendeley_settings.CLIENT_ID,
        refresh_token=refresh_token,
        code=code,
        expires_in=expires_in,

    )