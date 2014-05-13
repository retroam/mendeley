""" Factory boy factories for the Mendeley addon."""

from factory import SubFactory, Sequence
from tests.factories import ModularOdmFactory, UserFactory, ProjectFactory

from website.addons.mendeley.model import (
    MendeleyUserSettings, MendeleyNodeSettings
)

class MendeleyUserSettingsFactory(ModularOdmFactor):
    FACTOR_FOR = MendeleyUserSettings

    owner = SubFactory(UserFactory)
    access_token = Sequence(lambda n: 'abcdef{0}'.format(n))

class MendeleyNodeSettingsFactory(ModularOdmFactory):
    FACTORY_FOR = MendeleyNodeSettings

    owner = SubFactory(ProjectFactory)
    user_settings = SubFactory(MendeleyUserSettingsFactory)
    folder = 'COS papers'

