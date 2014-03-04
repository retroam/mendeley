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

    user_settings = fields.ForeignField(
        'addonmendeleyusersettings', backref='authorized'
    )

    registration_data = fields.DictionaryField()

    @property
    def short_url(self):
        if self.user:
            return '/'.join([self.user])

    def to_json(self, user):
        mendeley_user = user.get_addon('mendeley')
        rv = super(AddonMendeleyNodeSettings, self).to_json(user)
        rv.update({
            'mendeley_user': self.user or '',
            'user_has_authorization': mendeley_user and mendeley_user.has_auth,
            'show_submit': True,
        })
        if self.user_settings and self.user_settings.has_auth:
            rv.update({
                'authorized_user_name': self.user_settings.owner.fullname,
                'authorized_user_id': self.user_settings.owner._id,
                'authorized_mendeley_user': self.user_settings.mendeley_user,
                'disabled': self.user_settings.owner != user,
                'show_submit': (
                    self.user_settings.owner is None or
                    self.user_settings.owner == user
                ),
            })
        return rv

    #############
    # Callbacks #
    #############

    # def before_page_load(self, node, user):
    #     """
    #
    #     :param Node node:
    #     :param User user:
    #     :return str: Alert message
    #
    #     """
    #     # Quit if not contributor
    #     if not node.is_contributor(user):
    #         return
    #
    #     # Quit if not configured
    #     if self.user is None or self.repo is None:
    #         return
    #
    #     # Quit if no user authorization
    #     if self.user_settings is None:
    #         return
    #     connect = Mendeley.from_settings(self.user_settings)
    #     repo = connect.repo(self.user, self.repo)
    #
    #     # Quit if request failed
    #     if repo is None:
    #         return
    #
    #     node_permissions = 'public' if node.is_public else 'private'
    #     repo_permissions = 'private' if repo['private'] else 'public'
    #     if repo_permissions != node_permissions:
    #         message = (
    #             'Warnings: This OSF {category} is {node_perm}, but the Mendeley '
    #             'repo {user} / {repo} is {repo_perm}.'.format(
    #                 category=node.project_or_component,
    #                 node_perm=node_permissions,
    #                 repo_perm=repo_permissions,
    #                 user=self.user,
    #                 repo=self.repo,
    #             )
    #         )
    #         if repo_permissions == 'private':
    #             message += (
    #                 ' Users can view the contents of this private Mendeley '
    #                 'repository through this public project.'
    #             )
    #         else:
    #             message += (
    #                 ' The files in this Mendeley repo can be viewed on Mendeley '
    #                 '<a href="https://mendeley.com/{user}/{repo}/">here</a>.'
    #             ).format(
    #                 user=self.user,
    #                 repo=self.repo,
    #             )
    #         return message
    #
    # # TODO: Rename to before_remove_contributor_message
    # def before_remove_contributor(self, node, removed):
    #     """
    #
    #     :param Node node:
    #     :param User removed:
    #     :return str: Alert message
    #
    #     """
    #     if self.user_settings and self.user_settings.owner == removed:
    #         return (
    #             'The Mendeley add-on for this {category} is authenticated '
    #             'by {user}. Removing this user will also remove write access '
    #             'to Mendeley unless another contributor re-authenticates. You '
    #             'can download the contents of this repository before removing '
    #             'this contributor <a href="{url}">here</a>.'
    #         ).format(
    #             category=node.project_or_component,
    #             user=removed.fullname,
    #             url=node.api_url + 'mendeley/tarball/'
    #         )
    #
    # def after_remove_contributor(self, node, removed):
    #     """
    #
    #     :param Node node:
    #     :param User removed:
    #     :return str: Alert message
    #
    #     """
    #     if self.user_settings and self.user_settings.owner == removed:
    #
    #         # Delete OAuth tokens
    #         self.user_settings = None
    #         self.save()
    #
    #         #
    #         return (
    #             'Because the Mendeley add-on for this project was authenticated '
    #             'by {user}, authentication information has been deleted. You '
    #             'can re-authenticate on the <a href="{url}settings/">'
    #             'Settings</a> page.'.format(
    #                 user=removed.fullname,
    #                 url=node.url,
    #             )
    #         )
    #
    # def after_set_permissions(self, node, permissions):
    #     """
    #
    #     :param Node node:
    #     :param str permissions:
    #     :return str: Alert message
    #
    #     """
    #     if not mendeley_settings.SET_PRIVACY:
    #         return
    #
    #     connect = Mendeley.from_settings(self.user_settings)
    #
    #     data = connect.set_privacy(
    #         self.user, self.repo, permissions == 'private'
    #     )
    #     if data is None or 'errors' in data:
    #         repo = connect.repo(self.user, self.repo)
    #         if repo is not None:
    #             current_privacy = 'private' if repo['private'] else 'public'
    #         else:
    #             current_privacy = 'unknown'
    #         return (
    #             'Could not set privacy for repo {user}::{repo}. '
    #             'Current privacy status is {perm}.'.format(
    #                 user=self.user,
    #                 repo=self.repo,
    #                 perm=current_privacy,
    #             )
    #         )
    #
    #     return (
    #         'Mendeley repo {user}::{repo} made {perm}.'.format(
    #             user=self.user,
    #             repo=self.repo,
    #             perm=permissions,
    #         )
    #     )
    #
    # def before_fork(self, node, user):
    #     """
    #
    #     :param Node node:
    #     :param User user:
    #     :return str: Alert message
    #
    #     """
    #     if self.user_settings and self.user_settings.owner == user:
    #         return (
    #             'Because you have authenticated the Mendeley add-on for this '
    #             '{cat}, forking it will also transfer your authorization to '
    #             'the forked {cat}.'
    #         ).format(
    #             cat=node.project_or_component,
    #         )
    #     return (
    #         'Because this Mendeley add-on has been authenticated by a different '
    #         'user, forking it will not transfer authentication to the forked '
    #         '{cat}.'
    #     ).format(
    #         cat=node.project_or_component,
    #     )
    #
    # def after_fork(self, node, fork, user, save=True):
    #     """
    #
    #     :param Node node: Original node
    #     :param Node fork: Forked node
    #     :param User user: User creating fork
    #     :param bool save: Save settings after callback
    #     :return tuple: Tuple of cloned settings and alert message
    #
    #     """
    #     clone, _ = super(AddonMendeleyNodeSettings, self).after_fork(
    #         node, fork, user, save=False
    #     )
    #
    #     # Copy authentication if authenticated by forking user
    #     if self.user_settings and self.user_settings.owner == user:
    #         clone.user_settings = self.user_settings
    #         message = (
    #             'Mendeley authorization copied to forked {cat}.'
    #         ).format(
    #             cat=fork.project_or_component,
    #         )
    #     else:
    #         message = (
    #             'Mendeley authorization not copied to forked {cat}. You may '
    #             'authorize this fork on the <a href={url}>Settings</a> '
    #             'page.'
    #         ).format(
    #             cat=fork.project_or_component,
    #             url=fork.url + 'settings/'
    #         )
    #
    #     if save:
    #         clone.save()
    #
    #     return clone, message
    #
    # def before_register(self, node, user):
    #     """
    #
    #     :param Node node:
    #     :param User user:
    #     :return str: Alert message
    #
    #     """
    #     if self.user_settings:
    #         return (
    #             'Registering this {cat} will copy the authentication for its '
    #             'Mendeley add-on to the registered {cat}.'
    #         ).format(
    #             cat=node.project_or_component,
    #         )
    #
    # def after_register(self, node, registration, user, save=True):
    #     """
    #
    #     :param Node node: Original node
    #     :param Node registration: Registered node
    #     :param User user: User creating registration
    #     :param bool save: Save settings after callback
    #     :return tuple: Tuple of cloned settings and alert message
    #
    #     """
    #     clone, message = super(AddonMendeleyNodeSettings, self).after_register(
    #         node, registration, user, save=False
    #     )
    #
    #     # Copy foreign fields from current add-on
    #     clone.user_settings = self.user_settings
    #
    #     # Store current branch data
    #     if self.user and self.repo:
    #         connect = Mendeley.from_settings(self.user_settings)
    #         branches = connect.branches(self.user, self.repo)
    #         if branches is None:
    #             raise AddonError('Could not fetch repo branches.')
    #         clone.registration_data['branches'] = branches
    #
    #     if save:
    #         clone.save()
    #
    #     return clone, message
    #
    # #########
    # # Hooks #
    # #########
    #
    # def add_hook(self, save=True):
    #
    #     if self.user_settings:
    #         connect = Mendeley.from_settings(self.user_settings)
    #         hook = connect.add_hook(
    #             self.user, self.repo,
    #             'web',
    #             {
    #                 'url': urlparse.urljoin(
    #                     hook_domain,
    #                     os.path.join(
    #                         self.owner.api_url, 'mendeley', 'hook/'
    #                     )
    #                 ),
    #                 'content_type': 'json',
    #             }
    #         )
    #
    #         if hook:
    #             self.hook_id = hook['id']
    #             if save:
    #                 self.save()
    #
    # def delete_hook(self, save=True):
    #     """
    #
    #     :return bool: Hook was deleted
    #
    #     """
    #     if self.user_settings and self.hook_id:
    #         connect = Mendeley.from_settings(self.user_settings)
    #         response = connect.delete_hook(self.user, self.repo, self.hook_id)
    #         if response:
    #             self.hook_id = None
    #             if save:
    #                 self.save()
    #             return True
    #     return False
