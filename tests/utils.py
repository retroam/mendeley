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
                'library': {u'document_ids': [u'6147361191'],
                             u'documents': [{u'version': 1398096652, u'id': u'6147361191'}],
                             u'total_results': 1,
                             u'current_page': 0,
                             u'total_pages': 1,
                             u'items_per_page': 20},
                'folders': {u'parent': -1,
                              u'size': 1,
                              u'id': u'83330051',
                              u'version': u'1',
                              u'name': u'Cool Papers'
                    },
                'folder_details': {u'document_ids': [u'6147361191'], u'documents': [{u'version': 1398096652, u'id': u'6147361191'}],
                                    u'total_results': 1,
                                    u'current_page': 0,
                                    u'total_pages': 1,
                                    u'items_per_page': 20,
                                    u'folder_id': u'83330051',
                                    u'folder_version': u'1',
                                    u'folder_name': u'Cool Papers'},
                'document_details': {u'isAuthor': u'0',
                                u'identifiers': {u'pmid': u'23571845',
                                    u'doi': u'10.1038/nrn3475',
                                    u'isbn': u'1471-0048 (Electronic)\\r1471-003X (Linking)',
                                    u'issn': u'1471-0048'},
                   u'isbn': u'1471-0048 (Electronic)\\r1471-003X (Linking)',
                   u'abstract': u'A study with low statistical power has a reduced chance of detecting a true effect, '
                                u'but it is less well appreciated that low power also reduces the likelihood that a '
                                u'statistically significant result reflects a true effect. Here, we show that the '
                                u'average statistical power of studies in the neurosciences is very low. The '
                                u'consequences of this include overestimates of effect size and low '
                                u'reproducibility of results. There are also ethical dimensions to this problem, '
                                u'as unreliable research is inefficient and wasteful. Improving reproducibility in '
                                u'neuroscience is a key priority and requires attention to well-established but often'
                                u' ignored methodological principles.',
                   u'added': 1402411499,
                   u'year': u'2013',
                   u'keywords': [u'Humans',
                                 u'Neurosciences',
                                 u'Probability',
                                 u'Reproducibility of Results',
                                 u'Sample Size'],
                   u'isStarred': u'0',
                   u'id': u'6444921861',
                   u'discipline': u'Biological Sciences',
                   u'published_in': u'Nature reviews. Neuroscience',
                   u'title': u'Power failure: why small sample size undermines the reliability of neuroscience.',
                   u'editors': [],
                   u'deletionPending': u'0',
                   u'version': 1402411499,
                   u'pmid': u'23571845',
                   u'folders_ids': [],
                   u'issue': u'5',
                   u'files': [],
                   u'mendeley_url': u'http://www.mendeley.com/c/6444921861/p/22001711/button-2013-power-failure-'
                                    u'why-small-sample-size-undermines-the-reliability-of-neuroscience/',
                   u'tags': [],
                   u'volume': u'14',
                   u'isRead': u'0',
                   u'authors': [{u'surname': u'Button', u'forename': u'Katherine S'},
                                {u'surname': u'Ioannidis',u'forename': u'John P a'},
                                {u'surname': u'Mokrysz', u'forename': u'Claire'},
                                {u'surname': u'Nosek', u'forename': u'Brian a'},
                                {u'surname': u'Flint', u'forename': u'Jonathan'},
                                {u'surname': u'Robinson', u'forename': u'Emma S J'},
                                {u'surname': u'Munaf\xf2', u'forename': u'Marcus R'}],
                   u'pages': u'365-76',
                   u'publisher': u'Nature Publishing Group',
                   u'doi': u'10.1038/nrn3475',
                   u'url': u'http://www.ncbi.nlm.nih.gov/pubmed/23571845',
                   u'type': u'Journal Article',
                   u'notes': u'',
                   u'issn': u'1471-0048',
                   u'modified': 1402411499,
                   u'publication_outlet': u'Nature reviews. Neuroscience',
                   u'translators': [], u'subdiscipline': None}

    }

class MockMendeley(object):


    def library(self):
        return mock_responses['library']


    def folders(self):
        return mock_responses['folders']

    def folder_details(self, folder_id):
        if mock_responses['folders']['id'] == folder_id:
            ret = mock_responses['folder_details']
        else:
            ret = None
        return ret

    def document_details(self, document_id):
        if mock_responses['library']['document_ids'] == document_id:
            ret = mock_responses['document_details']
        else:
            ret = None
        return ret


