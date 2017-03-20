from django.conf import settings

ORGANIZATION_MODEL = getattr(settings, 'TIERS_ORGANIZATION_MODEL', 'organizations.Organization')
EXPIRED_REDIRECT_URL = getattr(settings, 'TIERS_EXPIRED_REDIRECT_URL', None)

ORGANIZATION_TIER_GETTER_NAME = getattr(settings, 'TIERS_ORGANIZATION_TIER_GETTER_NAME', None)

