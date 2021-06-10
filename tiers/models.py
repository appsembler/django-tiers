from datetime import timedelta
from functools import wraps

from django.utils import timezone
from django.utils.timesince import timeuntil
from django.db import models

from .app_settings import settings

from model_utils.models import TimeStampedModel
from model_utils import Choices


def set_default_expiration():
    return timezone.now() + timedelta(days=30)


def check_if_exempt(f):
    @wraps(f)
    def wrapper(self, **kwargs):
        if self.tier_enforcement_exempt:
            return False
        return f(self, **kwargs)
    return wrapper


class Tier(TimeStampedModel):
    TIERS = Choices(
        ('trial', 'TRIAL', 'Trial'),  # Expires in 30 days
        ('basic', 'BASIC', 'Basic'),
        ('pro', 'PRO', 'Professional'),
        ('premium', 'PREMIUM', 'Premium'),
    )

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
    tier_enforcement_grace_period = models.PositiveIntegerField(default=14)
    tier_expires_at = models.DateTimeField(
        default=set_default_expiration)

    def __str__(self):
        return 'Tier <org: {0} at tier: {1}>'.format(self.organization.name, self.name)

    class Meta:
        app_label = 'tiers'

    @check_if_exempt
    def has_tier_expired(self):
        """Helper function that checks whether a tier has expired"""
        return timezone.now() > self.tier_expires_at

    @check_if_exempt
    def has_tier_grace_period_expired(self):
        """Helper function that checks whether a tier's grace period has expired"""
        return (
            timezone.now() >
            (self.tier_expires_at + timedelta(days=self.tier_enforcement_grace_period)))

    @check_if_exempt
    def time_til_tier_expires(self, now=None):
        """Pretty prints time left til expiration"""
        return timeuntil(self.tier_expires_at, now)
