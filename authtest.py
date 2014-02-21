from requests_oauthlib import OAuth2Session
from framework import request

OAUTH_AUTHORIZE_URL = 'https://api-oauth2.mendeley.com/oauth/authorize'
OAUTH_ACCESS_TOKEN_URL = 'https://api-oauth2.mendeley.com/oauth/token'
# Mendeley application credentials
CLIENT_ID = '29'
CLIENT_SECRET = 'ID13I@-b8[z\\as8T'

# Mendeley access scope
SCOPE = ['all']
DOMAIN = 'http://0.0.0.0:5000/'
redirect_uri = 'http://0.0.0.0:5000/api/v1/addons/mendeley/callback/'
code = "UNzcye3PzZzBs88O-lhlbZqwuLE"

def oauth_start_url(user, node=None):
    """Get authorization URL for OAuth.

    :param User user: OSF user
    :param Node node: OSF node
    :return tuple: Tuple of authorization URL and OAuth state

    """

    uri_parts = [
        DOMAIN, 'api', 'v1', 'addons', 'mendeley',
        'callback'
    ]
    if node:
        uri_parts.append(node._id)
    redirect_uri = 'http://0.0.0.0:5000/api/v1/addons/mendeley/callback/%s/'



    session = OAuth2Session(
        CLIENT_ID,
        redirect_uri=redirect_uri,
        scope=SCOPE,
    )
    return session.authorization_url(OAUTH_AUTHORIZE_URL)


def oauth_get_token(code):
    """Get OAuth access token.

    :param str code: Authorization code from provider
    :return str: OAuth access token

    """
    session = OAuth2Session(
        CLIENT_ID,
        redirect_uri=redirect_uri,
    )


    return session.fetch_token(
        OAUTH_ACCESS_TOKEN_URL,
        client_secret=CLIENT_SECRET,
        code=code,
    )

user = None




oauth_get_token(code)