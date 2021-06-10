import logging

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.urls import NoReverseMatch, reverse

from .helpers import is_equal_or_sub_url, is_white_listed_url
from .models import Tier
from .app_settings import settings
from .waffle_utils import should_redirect_non_authenticated

try:
    import beeline
except ImportError:
    import tiers.instrumentation as beeline

log = logging.getLogger(__name__)


class TierMiddleware(MiddlewareMixin):
    """
    Django Tiers middleware
    """
    @beeline.traced(name="TiersMiddleware.process_request")
    def process_request(self, request):
        """
        Fetch organization from session and deny access to the system if the tier
        is expired
        """
        # If we're aleady on the url where we have to be, do nothing
        expired_redirect_url = settings.expired_redirect_url()
        if is_equal_or_sub_url(request_url=request.path, checked_url=expired_redirect_url):
            beeline.add_context_field("tiers.no_action_required", True)
            return

        # try/catch needed because the URLs don't necessarily exist both in AMC and edX
        try:
            # If we're trying to log out or release a hijacked user, don't redirect to expired page
            if request.path == reverse("release_hijack") or request.path == reverse("account_logout"):
                return
        except NoReverseMatch:
            pass

        if not request.user.is_authenticated:
            # Depending on the feature flag, we may redirect the non-logged in users
            if not should_redirect_non_authenticated():
                return

        # If the user has superuser privileges don't do anything
        if request.user.is_authenticated and request.user.is_superuser:
            return

        # If there is no organization in the sesssion fail silenty.
        # This should not happen.
        if not request.session.get('organization'):
            beeline.add_context_field("tiers.no_organization", True)
            return

        org = request.session['organization']
        beeline.add_context_field("tiers.organization", "{}".format(org))
        try:
            organization_tier_getter_name = settings.organization_tier_getter_name()
            if organization_tier_getter_name:
                tier = org.__getattribute__(organization_tier_getter_name)()
            else:
                tier = org.tier
        except Exception:
            # If the organization for some reason does not have a tier assigned
            # fail silently. This should not happen. We should always automatically create
            # a tier for each organization.
            beeline.add_context_field("tiers.organization_without_tier", True)
            log.exception("Organization has a problem with its Tier: {0}".format(org))
            return

        # Only display expiration warning for Trial tiers for now
        request.session['DISPLAY_EXPIRATION_WARNING'] = ((tier.name == Tier.TIERS.TRIAL) and
                                                         (not tier.tier_enforcement_exempt))
        request.session['TIER_EXPIRES_IN'] = tier.time_til_tier_expires()
        beeline.add_context_field("tiers.tier_expires_in", request.session['TIER_EXPIRES_IN'])
        # TODO: I'm not sure if we have to refresh the session info at this point somehow.
        request.session['TIER_EXPIRED'] = tier.has_tier_expired()
        beeline.add_context_field("tiers.tier_expired", request.session['TIER_EXPIRED'])
        # TODO: We should use request.TIER_NAME instead of meddling the session, but being consistent for now
        request.session['TIER_NAME'] = tier.name
        beeline.add_context_field("tiers.tier_name", tier.name)

        # TODO: I'm not sure if we have to refresh the session info at this point somehow.
        if tier.has_tier_expired():
            if expired_redirect_url and not is_white_listed_url(request.path):
                return redirect(expired_redirect_url)
