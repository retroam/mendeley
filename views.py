"""

"""


import os

import httplib as http


from framework import request, redirect
from framework.auth import get_current_user
from framework.auth.decorators import must_be_logged_in

from framework.exceptions import HTTPError



from website import models

from website.project.decorators import must_be_contributor
from website.project.decorators import must_be_contributor_or_public

from website.project.decorators import must_have_addon
from website.project.views.node import _view_project

from .api import Mendeley
from .auth import oauth_start_url, oauth_get_token, oauth_refresh_token

from citeproc.py2compat import *
from citeproc import CitationStylesStyle, CitationStylesBibliography
from citeproc import Citation, CitationItem
from citeproc import formatter
from citeproc.source.json import CiteProcJSON
from flask import Flask, send_file
import StringIO


MESSAGE_BASE = 'via the Open Science Framework'
MESSAGES = {
    'add': 'Added {0}'.format(MESSAGE_BASE),
    'update': 'Updated {0}'.format(MESSAGE_BASE),
    'delete': 'Deleted {0}'.format(MESSAGE_BASE),
}

CSL_PATH = '~/Documents/mendeley-oapi-example/citeproc/data/styles'

CITATION_STYLES = { 'American Political Science Association' : 'american-political-science-association',
                    'American Psychological Association' : 'apa',
                    'American Sociological Association' : 'american-sociological-association',
                    'Harvard Reference Format' : 'harvard1',
                    'IEEE' : 'ieee',
                    'Nature' : 'nature'}

EXPORT_FORMATS = ['bibtex', 'coins', 'bookmarks', 'refer', 'wikipedia']

@must_be_logged_in
def mendeley_set_user_config(*args, **kwargs):
    return {}


def _connect_to_library(mendeley_user, mendeley, user):

    code = None
    token = oauth_refresh_token(mendeley_user.oauth_refresh_token,
                                code,
                                user.user,
                               mendeley_user.oauth_token_expires,
                               mendeley_user.oauth_token,)

    mendeley_user.oauth_access_token = token['access_token']
    mendeley_user.oauth_refresh_token = token['refresh_token']
    mendeley_user.oauth_token_type = token['token_type']
    mendeley_user.oauth_token_expires = token['expires_in']

    connect = Mendeley.from_settings(mendeley.user_settings)
    return connect


def parse_library(connect, mendeley):

    user_library = connect.library(mendeley.user_settings)
    document_id = user_library['document_ids']
    doc_meta = []

    for idx in range(0, len(document_id)-1):
        meta = connect.document_details(mendeley.user_settings, document_id[idx])
        author = []
        second_line = ''
        for idy in range(0, len(meta['authors'])):
            author.append({
                'family':meta['authors'][idy]['surname'],
                'given': meta['authors'][idy]['forename'],
            })
            second_line = second_line + str(meta['authors'][idy]['forename']) + ' ' \
                           + str(meta['authors'][idy]['surname']) + ', '
        second_line = second_line[:-2]
        second_line = second_line + ' (' + str(meta.get('year', '0')) + ')'

        third_line = str(meta['published_in']) + ' ' \
            + str(meta['volume']) + ' '  \
            + '(' + str(meta.get('issue', '')) + ')' + ' ' + \
            str(meta.get('pages', ''))

        doc_meta.append({
            "author": author,
            "id": meta['id'],
            "issued": {
            "date-parts": [
                [
                    meta.get('year', '0'),
                    meta.get('month', '0'),
                    meta.get('day', '0'),
                ]
            ]
            },
            "title": meta.get('title', "").replace('.', ''),
            "type": meta.get('type', "").lower(),
            "abstract": meta.get('abstract', ""),
            "publisher": meta.get('published_in', ""),
            "volume": meta.get('volume', ""),
            "page": meta.get('pages', ""),
            "url": meta.get('url', " "),
            "second_line": second_line,
            "third_line": third_line,
             })

    return doc_meta


def _collection(client):
    connect = Mendeley.from_settings(client.user_settings)
    user_library = connect.library(client.user_settings)

    documentId = user_library['document_ids']
    doc_meta = []
    for idx in range(0,len(documentId)-1):
        meta = connect.document_details(client.user_settings,documentId[idx])
        doc_meta.append({
            "id": meta['id'],
            "title": meta['title'],
            "publisher": meta['published_in'],
            "type": "book",
            })

    return doc_meta

def _get_citation(library, document_id, style):

    bib_source = CiteProcJSON(library)
    bib_style = CitationStylesStyle(style)
    bibliography = CitationStylesBibliography(bib_style, bib_source, formatter.plain)

    # for idx in document_id:
    #     citation = Citation([CitationItem(idx)])
    #     bibliography.register(citation)

    citation = Citation([CitationItem('6147361191')])
    bibliography.register(citation)

    return bibliography

def _page_content(node, mendeley, branch=None, sha=None, hotlink=False, _connection=None):
    """Return the info to be rendered for a library.

    :param AddonMendeleyNodeSettings mendeley: The addon object.
    :param str branch: Git branch name.
    :param str sha: SHA hash.
    :param bool hotlink: Whether a direct download link from Mendeley is available.
        Disabled by default for now, since Mendeley sometimes passes the wrong
        content-type headers.
    :param Mendeley _connection: A Mendeley object for sending API requests. If None,
        a Mendeley object will be created from the user settings. This param is
        only exposed to allow for mocking the Mendeley API object.
    :returns: A dict of repo info to render on the page.

    """
    # Fail if Mendeley settings incomplete
    # if mendeley.user is None:
    #     return {}

    connect = Mendeley.from_settings(mendeley.user_settings)

    #
    # Check permissions if authorized
    has_access = False
    has_auth = bool(mendeley.user_settings and mendeley.user_settings.has_auth)
    if has_auth:
        has_access = True

    collection = ""
    view_string = "All Items"
    collection_names = []
    items = []
    error_statement = ""
    CITATION_STYLES = ""
    EXPORT_FORMAT = ""



    return {
        'complete': True,
        'gh_user': mendeley.user,
        'view_string': view_string,
        'collection_names':collection_names,
        'citation_styles': CITATION_STYLES,
        'export_formats':EXPORT_FORMAT,
        'error_statement': error_statement,
        'items': items,
        'collection':collection,
        'has_auth': has_auth,
        'has_access': has_access,
        'api_url': node.url,

    }


@must_be_contributor
@must_have_addon('mendeley', 'node')
def mendeley_set_config(*args, **kwargs):

    user = kwargs['user']

    mendeley_node = kwargs['node_addon']
    mendeley_user = mendeley_node.user_settings

    # If authorized, only owner can change settings
    if mendeley_user and mendeley_user.owner != user:
        raise HTTPError(http.BAD_REQUEST)

    return {}



@must_be_contributor_or_public
@must_have_addon('mendeley', 'node')
def mendeley_widget(*args, **kwargs):

    mendeley = kwargs['node_addon']
    connect = Mendeley.from_settings(mendeley.user_settings)

    # Check whether user has view access to repo
    complete = False
    if mendeley.user and mendeley.repo:
        repo = connect.repo(mendeley.user, mendeley.repo)
        if repo:
            complete = True

    if mendeley:
        rv = {
            'complete': complete,
            'short_url': mendeley.short_url,
        }
        rv.update(mendeley.config.to_json())
        return rv
    raise HTTPError(http.NOT_FOUND)


@must_be_contributor_or_public
@must_have_addon('mendeley', 'node')
def mendeley_page(*args, **kwargs):

    user = kwargs['auth']
    node = kwargs['node'] or kwargs['project']
    mendeley = kwargs['node_addon']
    mendeley_user = user.user.get_addon('mendeley')


    code = request.args.get('code')

    token = oauth_refresh_token(mendeley_user.oauth_refresh_token,
                                code,
                                user.user,
                               mendeley_user.oauth_token_expires,
                               mendeley_user.oauth_token,)

    mendeley_user.oauth_access_token = token['access_token']
    mendeley_user.oauth_refresh_token = token['refresh_token']
    mendeley_user.oauth_token_type = token['token_type']
    mendeley_user.oauth_token_expires = token['expires_in']

    library_connect = _connect_to_library(mendeley_user, mendeley, user)
    library = parse_library(library_connect, mendeley)

    data = _view_project(node, user, primary=True)

    rv = _page_content(node, mendeley)
    rv.update({
        'addon_page_js': mendeley_user.config.include_js.get('page'),
        'addon_page_css': mendeley_user.config.include_css.get('page'),
        'items': library,
        'citation_styles': CITATION_STYLES,
        'export_formats': EXPORT_FORMATS,
    })
    rv.update(mendeley_user.config.to_json())
    rv.update(data)

    return rv




# TODO: Remove unnecessary API calls

@must_be_contributor
@must_have_addon('mendeley', 'node')
def mendeley_add_user_auth(*args, **kwargs):

    user = kwargs['user']

    mendeley_user = kwargs['user_addon']
    mendeley_node = kwargs['node_addon']

    if mendeley_node is None or mendeley_user is None:
        raise HTTPError(http.BAD_REQUEST)

    mendeley_node.user_settings = mendeley_user
    mendeley_node.save()

    return {}


@must_be_logged_in
def mendeley_oauth_start(*args, **kwargs):

    user = get_current_user()

    nid = kwargs.get('nid') or kwargs.get('pid')
    node = models.Node.load(nid) if nid else None

    # Fail if node provided and user not contributor
    if node and not node.is_contributor(user):
        raise HTTPError(http.FORBIDDEN)

    user.add_addon('mendeley')
    mendeley_user = user.get_addon('mendeley')

    if node:

        mendeley_node = node.get_addon('mendeley')
        mendeley_node.user_settings = mendeley_user

        # Add webhook
        if mendeley_node.user and mendeley_node.repo:
            mendeley_node.add_hook()

        mendeley_node.save()

    authorization_url, state = oauth_start_url(user, node)

    mendeley_user.oauth_state = state
    mendeley_user.save()

    return redirect(authorization_url)


@must_have_addon('mendeley', 'user')
def mendeley_oauth_delete_user(*args, **kwargs):

    mendeley_user = kwargs['user_addon']

    # Revoke access token
    connect = Mendeley.from_settings(mendeley_user)
    connect.revoke_token()

    mendeley_user.oauth_access_token = None
    mendeley_user.oauth_token_type = None
    mendeley_user.save()

    return {}


@must_be_contributor
@must_have_addon('mendeley', 'node')
def mendeley_oauth_delete_node(*args, **kwargs):

    mendeley_node = kwargs['node_addon']
    user = models.User.load(kwargs.get('uid'))

    mendeley_node.user_settings = None
    mendeley_node.save()


    return {}


def mendeley_oauth_callback(*args, **kwargs):

    user = models.User.load(kwargs.get('uid'))
    node = models.Node.load(kwargs.get('nid'))

    raise Exception

    if user is None:
        raise HTTPError(http.NOT_FOUND)
    if kwargs.get('nid') and not node:
        raise HTTPError(http.NOT_FOUND)

    mendeley_user = user.get_addon('mendeley')
    if mendeley_user is None:
        raise HTTPError(http.BAD_REQUEST)

    if mendeley_user.oauth_state != request.args.get('state'):
        raise HTTPError(http.BAD_REQUEST)

    mendeley_node = node.get_addon('mendeley') if node else None

    code = request.args.get('code')
    if code is None:
        raise HTTPError(http.BAD_REQUEST)

    token = oauth_get_token(code,user)

    mendeley_user.oauth_state = None
    mendeley_user.oauth_access_token = token['access_token']
    mendeley_user.oauth_refresh_token = token['refresh_token']
    mendeley_user.oauth_token_type = token['token_type']
    mendeley_user.oauth_token_expires = token['expires_in']
    mendeley_user.oauth_token = token

    connect = Mendeley.from_settings(mendeley_user)
    user = connect.user()

    # mendeley_user.mendeley_user = user['login']

    mendeley_user.save()

    if mendeley_node:
        mendeley_node.user_settings = mendeley_user
        mendeley_node.save()

    if node:
        return redirect(os.path.join(node.url, 'settings'))
    return redirect('/settings/')

@must_be_contributor_or_public
@must_have_addon('mendeley', 'node')
def mendeley_export(*args, **kwargs):

    user = kwargs['auth']
    node = kwargs['node'] or kwargs['project']
    mendeley = kwargs['node_addon']
    mendeley_node = node.get_addon('mendeley')
    mendeley_user = user.user.get_addon('mendeley')

    library_connect = _connect_to_library(mendeley_user, mendeley, user)
    library = parse_library(library_connect, mendeley)

    if mendeley_node:

        keys = request.args.getlist('allKeys')
        format = request.args.get('format')

        if format not in EXPORT_FORMATS:
            raise HTTPError(http.BAD_REQUEST), "Export format not recognized"

        if keys:
            export = _get_citation(library, keys, format)
            export = export.bibliography()
            print export
        else:
            export = 'No Items specified'

        raise Exception
        strIO = StringIO.StringIO()
        strIO.write(str(export))
        strIO.seek(0)

        return send_file(strIO, attachment_filename="mendeley_export_"+format+".txt", as_attachment=True)

    else:
        raise HTTPError(http.BAD_REQUEST)

@must_be_contributor_or_public
@must_have_addon('mendeley', 'node')
def mendeley_citation(*args, **kwargs):

    user = kwargs['auth']
    node = kwargs['node'] or kwargs['project']
    mendeley = kwargs['node_addon']
    mendeley_node = node.get_addon('mendeley')
    mendeley_user = user.user.get_addon('mendeley')

    library_connect = _connect_to_library(mendeley_user, mendeley, user)
    library = parse_library(library_connect, mendeley)

    if mendeley_node:
        keys = request.json.get('allKeys')
        style = request.json.get('style')

        if CITATION_STYLES in style:
            style = CITATION_STYLES[style]
        else:
            raise HTTPError(http.BAD_REQUEST)

        if keys:
            citations = _get_citation(library, keys, style)
        else:
            citations = '<span>No Items specified</span>'

        results = {"citationText": citations}

        print citations

        return [results]

    else:
        raise HTTPError(http.BAD_REQUEST)
