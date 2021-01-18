import factory
from django.contrib.auth.models import User
from django.test import RequestFactory
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


def tiers_request_factory(organization=None):
    request = RequestFactory().get('/dashboard')
    request.session = {
        'organization': organization,
    }
    request.user = User()
    return request
