import os

from nose.tools import *

from framework.auth.decorators import Auth
from website.addons.mendeley.model import (
MendeleyUserSettings, MendeleyNodeSettings
)

from tests.base import DbTestCase, fake, URLLookup
from tests.factories import UserFactory, ProjectFactory
from website.addons.mendeley.tests.factories import (
MendeleyUserSettingsFactory, MendeleyNodeSettingsFactory
)

from website.app import init_app

app = init_app(set_backends=False, routes=True)
lookup = URLLookup(app)

class TestUserSettingsModel(DbTestCase):

    def setUp(self):
        self.user = UserFacory()

    def test_fields(self):

        user_settings = MendeleyUserSettings(
            access_token='12345',
            mendeley_id='abc',
            owner=self.user
        )
        user_settings.save()
        retrieved = MendeleyUserSettings.load(user_settings._primary_key)
        assert_true(retrieved.access_token)
        assert_true(retrieved.mendeley_id)
        assert_true(retrieved.owner)

    def test_has_auth(self):
        user_settings = MendeleyUserSettingsFactory(access_token=None)
        assert_false(user_settings.has_auth)
        user_settings.access_token = '12345'
        user_settings.save()
        assert_true(user_settings.has_auth)

    def test_clear_auth(self):
        None

    def test_delete(self):
        None

    def test_to_json(self):
        None

class TestMendeleyNodeSettingsModel(DbTestCase):

    def setUp(self):
        self.User = None

    def test_fields(self):
        None

    def test_has_auth(self):
        None

    def test_to_json(self):
        None

    def test_to_json(self):
        None

    def test_deauthorize(self):
        None

    def test_set_folder(self):
        None
