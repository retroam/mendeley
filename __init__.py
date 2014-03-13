from .model import AddonMendeleyUserSettings, AddonMendeleyNodeSettings
from .routes import settings_routes, page_routes, api_routes

USER_SETTINGS_MODEL = AddonMendeleyUserSettings
NODE_SETTINGS_MODEL = AddonMendeleyNodeSettings

ROUTES = [api_routes, settings_routes, page_routes]

SHORT_NAME = 'mendeley'
FULL_NAME = 'Mendeley'

OWNERS = ['user', 'node']

ADDED_TO = {
    'user': False,
    'node': False,
}

VIEWS = ['widget', 'page']
CONFIGS = ['user', 'node']

CATEGORIES = ['bibliography']

INCLUDE_JS = {
    'widget': ['jquery.mendeleyRepoWidget.js'],
    'page': ['mendeley.js'],
}

INCLUDE_CSS = {
    'widget': [],
    'page': ['mendeley.css'],
}

WIDGET_HELP = 'Mendeley Add-on Alpha'
