"""

"""

from framework.routing import Rule, json_renderer
from website.routes import OsfWebRenderer

from website.addons.mendeley import views

settings_routes = {
    'rules': [

        # Configuration
        Rule([
            '/project/<pid>/mendeley/settings/',
            '/project/<pid>/node/<nid>/mendeley/settings/',
        ], 'post', views.mendeley_set_config, json_renderer),

        Rule([
            '/project/<pid>/mendeley/widget/',
            '/project/<pid>/node/<nid>/mendeley/widget/',
        ], 'get', views.mendeley_widget, json_renderer),
        # Rule([
        #     '/project/<pid>/mendeley/file/<path:path>',
        #     '/project/<pid>/node/<nid>/mendeley/file/<path:path>',
        # ], 'get', views.mendeley_download_file, json_renderer),
        # Rule([
        #     '/project/<pid>/mendeley/',
        #     '/project/<pid>/node/<nid>/mendeley/',
        # ], 'get', views.mendeley_get_repo, json_renderer),
        # Rule([
        #     '/project/<pid>/mendeley/file/',
        #     '/project/<pid>/mendeley/file/<path:path>',
        #     '/project/<pid>/node/<nid>/mendeley/file/',
        #     '/project/<pid>/node/<nid>/mendeley/file/<path:path>',
        # ], 'post', views.mendeley_upload_file, json_renderer),
        # Rule([
        #     '/project/<pid>/mendeley/file/<path:path>',
        #     '/project/<pid>/node/<nid>/mendeley/file/<path:path>',
        # ], 'delete', views.mendeley_delete_file, json_renderer),
        # Rule([
        #     '/project/<pid>/mendeley/tarball/',
        #     '/project/<pid>/node/<nid>/mendeley/tarball/',
        # ], 'get', views.mendeley_download_starball, json_renderer, {'archive': 'tar'}, endpoint_suffix='__tar'),
        # Rule([
        #     '/project/<pid>/mendeley/zipball/',
        #     '/project/<pid>/node/<nid>/mendeley/zipball/',
        # ], 'get', views.mendeley_download_starball, json_renderer, {'archive': 'zip'}, endpoint_suffix='__zip'),

        # Rule([
        #     '/project/<pid>/mendeley/hook/',
        #     '/project/<pid>/node/<nid>mendeley/hook/',
        # ], 'post', views.mendeley_hook_callback, json_renderer),

        # OAuth: User
        Rule(
            '/settings/mendeley/oauth/',
            'get', views.mendeley_oauth_start, json_renderer,
            endpoint_suffix='__user'),
        Rule(
            '/settings/mendeley/oauth/delete/', 'post',
            views.mendeley_oauth_delete_user, json_renderer,
        ),

        # OAuth: Node
        Rule([
            '/project/<pid>/mendeley/oauth/',
            '/project/<pid>/node/<nid>/mendeley/oauth/',
        ], 'get', views.mendeley_oauth_start, json_renderer),
        Rule([
            '/project/<pid>/mendeley/user_auth/',
            '/project/<pid>/node/<nid>/mendeley/user_auth/',
        ], 'post', views.mendeley_add_user_auth, json_renderer),
        Rule([
            '/project/<pid>/mendeley/oauth/delete/',
            '/project/<pid>/node/<nid>/mendeley/oauth/delete/',
        ], 'post', views.mendeley_oauth_delete_node, json_renderer),

        # OAuth: General
        Rule([
            '/addons/mendeley/callback/<uid>/',
            '/addons/mendeley/callback/<uid>/<nid>/',
        ], 'get', views.mendeley_oauth_callback, json_renderer),
    ],
    'prefix': '/api/v1',
}

api_routes = {
    'rules': [
        # # Route from which to get the hgrid data
        # Rule([
        #     '/project/<pid>/mendeley/hgrid/',
        #     '/project/<pid>/node/<nid>/mendeley/hgrid/',
        # ], 'get', views.mendeley_hgrid_data, json_renderer),
        #
        # Rule([
        #     '/project/<pid>/mendeley/hgrid/<path:path>/',
        #     '/project/<pid>/node/<nid>/mendeley/hgrid/<path:path>/',
        # ], 'get', views.mendeley_hgrid_data_contents, json_renderer),

    ],
    'prefix': '/api/v1'
}

page_routes = {
    'rules': [
        Rule([
            '/project/<pid>/mendeley/',
            '/project/<pid>/node/<nid>/mendeley/',
        ], 'get', views.mendeley_page, OsfWebRenderer('../addons/mendeley/templates/mendeley_page.mako')),
        Rule([
            '/project/<pid>/mendeley/getCitation',
            '/project/<pid>/node/<nid>/getCitation',
        ], 'get', views.mendeley_citation, OsfWebRenderer('../addons/mendeley/templates/mendeley_page.mako')),
        Rule([
            '/project/<pid>/mendeley/getExport',
            '/project/<pid>/node/<nid>/getExport',
        ], 'get', views.mendeley_export, OsfWebRenderer('../addons/mendeley/templates/mendeley_page.mako')),
    ],
}
