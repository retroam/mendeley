import mock
from contextlib import contextmanager

from webtest_plus import TestApp

from framework import storage
from framework.mongo import db, set_up_storage

import website
from website.addons.base.testing import AddonTestCase
from website.addons.mendeley import MODELS


app = website.app.init_app(
    routes=True, set_backends=False, settings_module='website.settings'
)


def init_storage():
    set_up_storage(MODELS, storage_class=storage.MongoStorage, db=db)


class MendeleyAddonTestCase(AddonTestCase):
    ADDON_SHORT_NAME = 'mendeley'

    def create_app(self):
        return TestApp(app)

    def set_user_settings(self, settings):
        settings.access_token = '12345abcd'
        settings.mendeley_user = 'mendeleyuser'

    def set_node_settings(self, settings):
        settings.folder = 'foo'

mock_responses = {

    }