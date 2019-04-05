import factory
from factory.django import DjangoModelFactory

from tiers.models import Tier
from fake_organizations.models import Organization


class OrganizationFactory(DjangoModelFactory):
    class Meta(object):
        model = Organization

    name = factory.Sequence('organization name {}'.format)


class TierFactory(DjangoModelFactory):
    class Meta(object):
        model = Tier

    organization = factory.SubFactory(OrganizationFactory)
