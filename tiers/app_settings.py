from django.conf import settings

TIERS_ORGANIZATION_MODEL = getattr(settings, 'ORGANIZATION_MODEL', 'organizations.Organization')

