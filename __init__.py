from .model import AddonMendeleyUserSettings, AddonMendeleyNodeSettings
from .routes import settings_routes, page_routes, api_routes



MODELS = [
    model.AddonMendeleyUserSettings,
    model.AddonMendeleyNodeSettings,
]

USER_SETTINGS_MODEL = model.AddonMendeleyUserSettings
NODE_SETTINGS_MODEL = model.AddonMendeleyNodeSettings

ROUTES = [routes.api_routes, routes.settings_routes, routes.page_routes]


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
