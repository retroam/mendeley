"""

"""

import os
import urlparse

from framework import fields

from website import settings
from website.addons.base import AddonUserSettingsBase, AddonNodeSettingsBase
from website.addons.base import AddonError

from . import settings as mendeley_settings
from .api import Mendeley



class AddonMendeleyUserSettings(AddonUserSettingsBase):

    mendeley_user = fields.StringField()

    oauth_state = fields.StringField()
    oauth_access_token = fields.StringField()
    oauth_refresh_token = fields.StringField()
    oauth_token_type = fields.StringField()
    oauth_token_expires = fields.StringField()
    oauth_token = fields.StringField()


    @property
    def has_auth(self):
        return self.oauth_access_token is not None

    def to_json(self, user):
        rv = super(AddonMendeleyUserSettings, self).to_json(user)
        rv.update({
            'authorized': self.has_auth,
            'authorized_mendeley_user': self.mendeley_user if self.mendeley_user else '',
            'show_submit': False,
        })
        return rv

class AddonMendeleyNodeSettings(AddonNodeSettingsBase):

    user = fields.StringField()
    folder = fields.StringField()

    user_settings = fields.ForeignField(
        'addonmendeleyusersettings', backref='authorized'
    )

    registration_data = fields.DictionaryField()

    @property
    def short_url(self):
        if self.user:
            return '/'.join([self.user])

    def to_json(self, user):
        rv = super(AddonMendeleyNodeSettings, self).to_json(user)
        user_settings = user.get_addon('mendeley')

        rv.update({
            'user_has_auth': user_settings and user_settings.has_auth,
            'is_registration': self.owner.is_registration,
        })
        if self.user_settings and self.user_settings.has_auth:
            owner = self.user_settings.owner
            if user_settings and user_settings.owner == owner:
                connection = Mendeley.from_settings(user_settings)
                user_folders = connection.folders(user_settings)
                user_folders_name = []

                for idx in range(0, len(user_folders)):
                    user_folder = '{0} / {1}'.format(self.user_settings.mendeley_user, user_folders[idx]['name'])
                    user_folders_name.append(user_folder)


                rv.update({
                    'node_has_auth': True,
                    'mendeley_user': self.user or '',
                    'mendeley_folder_full_name': '{0} / {1}'.format(self.user, self.folder),
                    'auth_osf_name': owner.fullname,
                    'auth_osf_url': owner.url,
                    'auth_osf_id': owner._id,
                    'mendeley_user_name': self.user_settings.mendeley_user,
                    'mendeley_user_url': 'https://mendeley.com/profiles/{0}'.format(self.user_settings.mendeley_user),
                    'is_owner': owner == user,
                    'folder_names': user_folders_name,
                })
        return rv

