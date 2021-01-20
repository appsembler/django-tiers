from django.conf import settings as django_settings


class Settings:
    """
    Utility class to get the settings
    """

    def organization_model(self):
        return getattr(django_settings, 'TIERS_ORGANIZATION_MODEL', 'organizations.Organization')

    def expired_redirect_url(self):
        return getattr(django_settings, 'TIERS_EXPIRED_REDIRECT_URL', None)

    def organization_tier_getter_name(self):
        return getattr(django_settings, 'TIERS_ORGANIZATION_TIER_GETTER_NAME', None)

    def redirect_white_list(self):
        return getattr(django_settings, 'TIERS_REDIRECT_WHITELIST', [
            '/admin'
        ])


settings = Settings()
