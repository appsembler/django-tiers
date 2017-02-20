from datetime import datetime, timedelta

import factory
from factory.django import DjangoModelFactory

from tiers.models import Tier, set_default_expiration
from organizations.models import Organization


class OrganizationFactory(DjangoModelFactory):
    class Meta(object):
        model = Organization

    name = factory.Sequence('organization name {}'.format)


class TierFactory(DjangoModelFactory):
    class Meta(object):
        model = Tier

    name = Tier.TIERS.TRIAL
    organization = factory.SubFactory(OrganizationFactory)

    tier_enforcement_exempt = False
    tier_enforcement_grace_period = 14
    tier_expires_at = datetime.now() + timedelta(days=30)

