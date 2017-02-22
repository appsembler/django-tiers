from django.conf import settings
from django.shortcuts import redirect

from .models import Tier


class TierMiddleware(object):
    """
    Django Tiers middleware
    """
    def process_request(self, request):
        """
        Fetch organization from session and deny access to the system if the tier
        is expired
        """
        if not request.user.is_authenticated():
            return

        if not request.session.get('organization'):
            return

        org = request.session['organization']
        tier = org.tier
        if tier.has_tier_expired():
            if tier.name == Tier.TIERS.TRIAL:
                request.session['DISPLAY_EXPIRATION_WARNING'] = True
                request.session['TIER_EXPIRES_IN'] = tier.time_til_tier_expires()
                return redirect(settings.TIER_EXPIRED_REDIRECT_URL)

