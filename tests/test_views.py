import mock
import unittest
from nose.tools import *
from webtest_plus import TestApp

import website.app
from tests.base import DbTestCase

from tests.factories import ProjectFactory, AuthUserFactory

from website.addons.base import AddonError
from website.addons.mendeley.tests.utils import create_mock_mendeley
from website.addons.mendeley import views


from framework.auth.decorators import Auth
from website.addons.mendeley import settings as mendeley_settings


app = website.app.init_app(
    routes=True, set_backends=False, settings_module='website.settings'
)

mendeley_mock = create_mock_mendeley(project=436)


class TestViewsConfig(DbTestCase):

    def setUp(self):

        super(TestViewsConfig, self).setUp()

        self.app = TestApp(app)
        self.user = AuthUserFactory()
        self.consolidated_auth = Auth(user=self.user)
        self.auth = ('test', self.user.api_keys[0]._primary_key)
        self.project = ProjectFactory(creator=self.user)

        self.non_authenticator = AuthUserFactory()
        self.project.add_contributor(
            contributor=self.non_authenticator,
            auth=Auth(self.project.creator),
        )

        self.project.add_addon('mendeley', auth=self.consolidated_auth)
        self.project.creator.add_addon('mendeley')
        self.node_settings = self.project.get_addon('mendeley')
        self.user_settings = self.project.creator.get_addon('mendeley')
        self.user_settings.oauth_access_token = 'legittoken'
        self.user_settings.oauth_access_token_secret = 'legittoken'
        self.user_settings.save()
        self.node_settings.user_settings = self.user_settings
        self.node_settings.mendeley_id = '123456'
        self.node_settings.mendeley_type = 'project'
        self.node_settings.mendeley_title = 'OVER9000'
        self.node_settings.save()

        self.mendeley = create_mock_mendeley('test')

    def test_config_no_change(self):
        num = len(self.project.logs)
        url = '/api/v1/project/{0}/mendeley/settings/'.format(self.project._id)
        rv = self.app.post_json(
            url, {'mendeley_value': 'project_123456', 'mendeley_title': 'OVER9000'}, auth=self.user.auth)
        self.project.reload()

        assert_equal(rv.status_int, 200)
        assert_equal(len(self.project.logs), num)

    def test_config_change(self):
        num = len(self.project.logs)
        url = '/api/v1/project/{0}/mendeley/settings/'.format(self.project._id)
        rv = self.app.post_json(
            url, {'mendeley_value': 'project_9001', 'mendeley_title': 'IchangedbecauseIcan'}, auth=self.user.auth)
        self.project.reload()
        self.node_settings.reload()

        assert_equal(rv.status_int, 200)
        assert_equal(self.node_settings.mendeley_id, '9001')
        assert_equal(len(self.project.logs), num + 1)
        assert_equal(self.project.logs[num].action, 'mendeley_content_linked')

    def test_config_unlink(self):
        url = '/api/v1/project/{0}/mendeley/unlink/'.format(self.project._id)
        rv = self.app.post(url, auth=self.user.auth)
        self.node_settings.reload()
        self.project.reload()

        assert_equal(self.project.logs[-1].action, 'mendeley_content_unlinked')
        assert_equal(rv.status_int, 200)
        assert_true(self.node_settings.mendeley_id == None)

    def test_config_unlink_no_node(self):
        self.node_settings.user_settings = None
        self.node_settings.save()
        self.node_settings.reload()
        url = '/api/v1/project/{0}/mendeley/unlink/'.format(self.project._id)
        rv = self.app.post(url, expect_errors=True, auth=self.user.auth)
        self.project.reload()

        assert_equal(self.node_settings.mendeley_id, '123456')
        assert_not_equal(self.project.logs[-1].action, 'mendeley_content_unlinked')
        assert_equal(rv.status_int, 400)


class TestUtils(DbTestCase):

    def setUp(self):
        super(TestUtils, self).setUp()

        self.app = TestApp(app)
        self.user = AuthUserFactory()
        self.consolidated_auth = Auth(user=self.user)
        self.auth = ('test', self.user.api_keys[0]._primary_key)
        self.project = ProjectFactory(creator=self.user)

        self.non_authenticator = AuthUserFactory()
        self.project.add_contributor(
            contributor=self.non_authenticator,
            auth=Auth(self.project.creator),
        )

        self.project.add_addon('mendeley', auth=self.consolidated_auth)
        self.project.creator.add_addon('mendeley')
        self.node_settings = self.project.get_addon('mendeley')
        self.user_settings = self.project.creator.get_addon('mendeley')
        self.user_settings.oauth_access_token = 'legittoken'
        self.user_settings.oauth_access_token_secret = 'legittoken'
        self.user_settings.save()
        self.node_settings.user_settings = self.user_settings
        self.node_settings.mendeley_id = '436'
        self.node_settings.mendeley_type = 'project'
        self.node_settings.save()






class TestViewsAuth(DbTestCase):

    def setUp(self):
        super(TestViewsAuth, self).setUp()

        self.app = TestApp(app)
        self.user = AuthUserFactory()
        self.consolidated_auth = Auth(user=self.user)
        self.auth = ('test', self.user.api_keys[0]._primary_key)
        self.project = ProjectFactory(creator=self.user)

        self.non_authenticator = AuthUserFactory()
        self.project.add_contributor(
            contributor=self.non_authenticator,
            auth=Auth(self.project.creator),
        )

        self.project.add_addon('mendeley', auth=self.consolidated_auth)
        self.project.creator.add_addon('mendeley')
        self.node_settings = self.project.get_addon('mendeley')
        self.user_settings = self.project.creator.get_addon('mendeley')
        self.node_settings.user_settings = self.user_settings
        self.node_settings.mendeley_id = '436'
        self.node_settings.mendeley_type = 'project'
        self.node_settings.save()

    #TODO Finish me, would require a lot of mocking it seems.
    def test_oauth_fail(self):
        url = '/api/v1/project/{0}/mendeley/oauth'.format(self.project._id)
        rv = self.app.get(url, auth=self.user.auth).maybe_follow()
        pass


    #TODO Finish me
    def test_oauth_bad_token(self):
        pass
