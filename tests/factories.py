""" Factory boy factories for the Mendeley addon."""

from factory import SubFactory, Sequence
from tests.factories import ModularOdmFactory, UserFactory, ProjectFactory

from website.addons.mendeley.model import (
    AddonMendeleyUserSettings, AddonMendeleyNodeSettings
)

class MendeleyUserSettingsFactory(ModularOdmFactor):
    FACTOR_FOR = AddonMendeleyUserSettings

    owner = SubFactory(UserFactory)
    access_token = Sequence(lambda n: 'abcdef{0}'.format(n))

class MendeleyNodeSettingsFactory(ModularOdmFactory):
    FACTORY_FOR = AddonMendeleyNodeSettings

    owner = SubFactory(ProjectFactory)
    user_settings = SubFactory(MendeleyUserSettingsFactory)
    folder = 'COS papers'

