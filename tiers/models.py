from datetime import timedelta

from django.utils import timezone
from django.db import models

from model_utils.models import TimeStampedModel
from model_utils import Choices


from .app_settings import settings
from .tier_info import TierInfo


def set_default_expiration(now=None):
    if not now:
        now = timezone.now()

    return now + timedelta(days=30)


class Tier(TimeStampedModel):
    TIERS = Choices(*[
        (tier.id, tier.id.upper(), tier.name)
        for tier in TierInfo.TIERS
    ])

    name = models.CharField(
        max_length=255,
        choices=TIERS,
        default=TIERS.TRIAL)
    organization = models.OneToOneField(
        settings.organization_model(),
        related_name='tier',
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING)
    tier_enforcement_exempt = models.BooleanField(default=False)
    tier_enforcement_grace_period = models.PositiveIntegerField(
        # TODO: Remove deprecated field https://github.com/appsembler/django-tiers/issues/36
        default=14,
    )
    tier_expires_at = models.DateTimeField(
        default=set_default_expiration)

    def __str__(self):
        return 'Tier <org: {0} at tier: {1}>'.format(self.organization.name, self.name)

    class Meta:
        app_label = 'tiers'

    def get_tier_info(self):
        return TierInfo(
            tier=self.name,
            subscription_ends=self.tier_expires_at,
            always_active=self.tier_enforcement_exempt,
        )

    def has_tier_expired(self, now=None):
        """Helper function that checks whether a tier has expired"""
        return self.get_tier_info().has_subscription_ended(now=now)

    def time_til_tier_expires(self, now=None):
        """Pretty prints time left til expiration"""
        return self.get_tier_info().time_til_expiration(now=now)
