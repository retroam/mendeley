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
from tests.base import DbTestCase, URLLookup, assert_is_redirect
from tests.factories import AuthUserFactory


from website.addons.mendeley.tests.utils import (
    MendeleyAddonTestCase, app, mock_responses, MockMendeley
)

lookup = URLLookup(app)
mock_client = MockMendeley()

class TestAuthViews(DbTestCase):

    def setUp(self):
        return None

    def test_mendeley_oauth_start(self):
        return None

    def test_mendeley_oauth_finish(self):
        return None

    def test_mendeley_oauth_delete_user(self):
        return None


class TestConfigViews(MendeleyAddonTestCase):

    def test_mendeley_config_get(self):
        return None

    def test_mendeley_deauthorize(self):
        return None

    def test_mendeley_import_user_auth_add_a_log(self):
        return None

    def test_mendeley_get_share_emails(self):
        return None

    def test_mendeley_get_share_emails_returns_error_if_not_authorize(self):
        return None

    def test_mendeley_get_share_emails_requires_user_addon(self):
        return None

class TestFilebrowserViews(MendeleyAddonTestCase):

    def test_mendeley_addon_folder(self):
        return None




