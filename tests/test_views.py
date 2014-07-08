"""Views tests for the Mendeley addon."""

import os
import unittest
from nose.tools import *
import mock
import httplib
import datetime

from werkzeug import FileStorage
from webtest_plus import TestApp
from framework.auth.decorators import Auth
from website.util import api_url_for
from website.project.model import NodeLog
from tests.base import OsfTestCase, assert_is_redirect
from tests.factories import AuthUserFactory, ProjectFactory
from website.addons.mendeley import views

from website.addons.mendeley.tests.utils import (
    MendeleyAddonTestCase, app, mock_responses, MockMendeley
)

mock_client = MockMendeley()


class TestAuthViews(OsfTestCase):

    def setUp(self):
        self.app = TestApp(app)
        self.user = AuthUserFactory()
        self.app.authenticate(*self.user.auth)


    def test_mendeley_oauth_start(self):
        self.user.add_addon('mendeley')
        settings = self.user.get_addon('mendeley')
        settings.access_token = '12345abc'
        print settings.has_auth
        settings.save()
       # assert_true(settings.has_auth)
        url = views.mendeley_oauth_start(self)
        print url



    def test_mendeley_oauth_delete_user(self):
        pass

    def test_mendeley_oauth_delete_node(self):
        pass

    def test_mendeley_oauth_callback(self):
        pass


class TestConfigViews(MendeleyAddonTestCase):

    def test_mendeley_set_config(self):
        pass

    def test_mendeley_add_user_auth(self):
        pass


class TestPageViews(MendeleyAddonTestCase):

    def test_mendeley_page(self):
        pass

    def test_mendeley_export(self):
        pass

    def test_mendeley_citation(self):
        pass




