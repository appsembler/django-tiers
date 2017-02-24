import logging

from django.shortcuts import redirect

from .models import Tier
from .app_settings import EXPIRED_REDIRECT_URL


log = logging.getLogger(__name__)


def clear_expiration_from_session(session):
    KEYS = ['DISPLAY_EXPIRATION_WARNING', 'TIER_EXPIRES_IN']
    for key in KEYS:
        try:
            del session[key]
        except KeyError:
            pass


class TierMiddleware(object):
    """
    Django Tiers middleware
    """
    def process_request(self, request):
        """
        Fetch organization from session and deny access to the system if the tier
        is expired
        """
        # Nothing to do if the user is not logged in
        if not request.user.is_authenticated():
            return

        # If the user has superuser privileges don't do anything
        if request.user.is_superuser:
            return

        # If there is not organization in the sesssion fail silenty.
        # This should not happen.
        if not request.session.get('organization'):
            return

        org = request.session['organization']
        try:
            tier = org.tier
        except:
            # If the organization for some reason does not have a tier assigned
            # fail silently. This should not happen. We should always automatically create
            # a tier for each organization.
            log.error("Organization wihout Tier: {0}".format(org))
            return

        # TODO: I'm not sure if we have to refresh the session info at this point somehow.
        if tier.has_tier_expired():
            if tier.name == Tier.TIERS.TRIAL:
                request.session['DISPLAY_EXPIRATION_WARNING'] = True
                request.session['TIER_EXPIRES_IN'] = tier.time_til_tier_expires()
                if EXPIRED_REDIRECT_URL is None:
                    return
                else:
                    return redirect(EXPIRED_REDIRECT_URL)
        else:
            clear_expiration_from_session(request.session)
            return

