import os

from nose.tools import *

from framework.auth.decorators import Auth
from website.addons.mendeley.model import (
AddonMendeleyUserSettings, AddonMendeleyNodeSettings
)

from tests.base import OsfTestCase, fake
from tests.factories import UserFactory, ProjectFactory
from website.addons.mendeley.tests.factories import (
MendeleyUserSettingsFactory, MendeleyNodeSettingsFactory)

from website.app import init_app

app = init_app(set_backends=False, routes=True)


class TestUserSettingsModel(OsfTestCase):

    def setUp(self):
        self.user = UserFactory()

    def test_fields(self):

        user_settings = MendeleyUserSettingsFactory(
            oauth_access_token='12345',
            mendeley_user='abc',
            owner=self.user
        )
        user_settings.save()
        retrieved = AddonMendeleyUserSettings.load(user_settings._primary_key)
        assert_true(retrieved.oauth_access_token)
        assert_true(retrieved.mendeley_user)
        assert_true(retrieved.owner)

    def test_has_auth(self):
        user_settings = MendeleyUserSettingsFactory(oauth_access_token=None)
        assert_false(user_settings.has_auth)
        user_settings.oauth_access_token = '12345'
        user_settings.save()
        assert_true(user_settings.has_auth)

    def test_clear_auth(self):
        user_settings = MendeleyUserSettingsFactory(oauth_access_token='abcde')
        assert_true(user_settings.oauth_access_token)
        user_settings.clear_auth()
        user_settings.save()
        assert_false(user_settings.oauth_access_token)
        assert_false(user_settings.mendeley_user)

    def test_delete(self):
        user_settings = MendeleyUserSettingsFactory()
        assert_true(user_settings.has_auth)
        user_settings.delete()
        user_settings.save()
        assert_false(user_settings.oauth_access_token)
        assert_false(user_settings.mendeley_user)

    def test_to_json(self):
        user_settings = MendeleyUserSettingsFactory(mendeley_user='abc')
        result = user_settings.to_json(user_settings)
        assert_equal(result['authorized'], user_settings.has_auth)
        assert_equal(result['authorized_mendeley_user'], user_settings.mendeley_user)


class TestMendeleyNodeSettingsModel(OsfTestCase):

    def setUp(self):
        self.user = UserFactory()
        self.user.add_addon('mendeley')
        self.user.save()
        self.user_settings = self.user.get_addon('mendeley')
        self.project = ProjectFactory()
        self.node_settings = MendeleyNodeSettingsFactory(
            user_settings=self.user_settings,
            owner=self.project
        )

    def test_fields(self):
        node_settings = AddonMendeleyNodeSettings(user_settings=self.user_settings)
        node_settings.save()
        assert_true(node_settings.user_settings)
        assert_equal(node_settings.user_settings.owner, self.user)
        assert_true(hasattr(node_settings, 'folder'))

    # def test_shorturl(self):
    #     node_settings = AddonMendeleyNodeSettings(user_settings=self.user_settings)
    #     print self.user
    #     print node_settings.short_url
    #     assert_equal(node_settings.short_url, '/'.join([self.user]))


    # def test_has_auth(self):
    #     None
    #

    def test_to_json(self):
        node_settings = self.node_settings
        user = self.user
        result = node_settings.to_json(user)
        assert_equal(result['addon_short_name'], 'mendeley')




    # def test_to_json(self):
    #     None
    #
    # def test_deauthorize(self):
    #     None
    #
    # def test_set_folder(self):
    #     None
