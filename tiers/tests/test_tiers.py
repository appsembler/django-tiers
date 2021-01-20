from __future__ import unicode_literals

import re
from waffle.testutils import override_switch

from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.test.client import RequestFactory
from mock import patch, Mock, PropertyMock

from tiers.tests.factories import TierFactory
from tiers.middleware import TierMiddleware
from tiers.waffle_utils import REDIRECT_NON_AUTHENTICATED


class TiersTests(TestCase):
    """
    Tests for the Tier model.
    """

    def test_non_expired_tier(self):
        t = TierFactory()
        assert t.tier_enforcement_exempt is False
        assert t.has_tier_expired() is False
        assert t.has_tier_grace_period_expired() is False

    def test_expired_tier(self):
        t = TierFactory(tier_expires_at=(datetime.now() - timedelta(days=2)))
        assert t.tier_enforcement_exempt is False
        assert t.has_tier_expired() is True
        assert t.has_tier_grace_period_expired() is False

    def test_expired_grade_period(self):
        t = TierFactory(tier_expires_at=(datetime.now() - timedelta(days=20)))
        assert t.tier_enforcement_exempt is False
        assert t.has_tier_expired() is True
        assert t.has_tier_grace_period_expired() is True

    def test_exemption(self):
        t = TierFactory(
            tier_enforcement_exempt=True,
            tier_expires_at=(datetime.now() - timedelta(days=20)))
        assert t.tier_enforcement_exempt is True
        assert t.has_tier_expired() is False
        assert t.has_tier_grace_period_expired() is False

    def test_expire_message(self):
        """
        Ensures that `has_tier_grace_period_expired` works well.

        This function uses regexps match what the Django `timeuntil` returns.
        The `avoid_wrapping` function has more details in the docstring.
        """
        t = TierFactory.create(tier_expires_at=datetime(2019, 2, 5) + timedelta(days=30))
        assert t.tier_expires_at == datetime(2019, 3, 7)

        message = t.time_til_tier_expires(now=datetime(2019, 2, 6))
        assert re.match('4.*weeks,.*1.*day', message), 'Should handle long time well'

        message = t.time_til_tier_expires(now=datetime(2019, 3, 4, 0, 8, 0))
        assert re.match(r'2.*days,.*23.*hours', message), 'Should short time well'

        message = t.time_til_tier_expires(now=datetime(2020, 2, 6))
        assert re.match('0.*minutes', message), 'Should handle future time well.'


@patch.object(User, 'is_authenticated', PropertyMock(return_value=True))
@patch('tiers.middleware.reverse', Mock(return_value='/something'))
class TestMiddlewareTests(TestCase):
    """
    TiersMiddleware tests with a non-expired trial Tier.
    """

    def setUp(self):
        super(TestMiddlewareTests, self).setUp()
        self.middleware = TierMiddleware()
        self.tier = TierFactory.create(tier_expires_at=datetime.now()+timedelta(days=40))
        self.request = RequestFactory().get('/dashboard')
        self.request.session = {'organization': self.tier.organization}
        self.user = User()
        self.request.user = self.user

    def test_empty_by_default_attributes(self):
        default = object()
        for attrib in ['DISPLAY_EXPIRATION_WARNING', 'TIER_EXPIRES_IN', 'TIER_EXPIRED', 'TIER_NAME']:
            assert self.request.session.get(attrib, default) is default

    def test_added_session_attribs(self):
        self.middleware.process_request(self.request)
        assert not self.request.session['TIER_EXPIRED']
        assert self.request.session['TIER_EXPIRES_IN'] == self.tier.time_til_tier_expires()
        assert self.request.session['DISPLAY_EXPIRATION_WARNING']
        assert self.request.session['TIER_NAME'] == 'trial'


@patch('tiers.middleware.reverse', Mock(return_value='/something'))
class TestExpiredTierMiddleware(TestCase):
    """
    TiersMiddleware tests with an expired trial Tier.
    """

    def setUp(self):
        super(TestExpiredTierMiddleware, self).setUp()
        self.middleware = TierMiddleware()
        self.tier = TierFactory.create(tier_expires_at=datetime.now() - timedelta(days=40))
        self.request = RequestFactory().get('/dashboard')
        self.request.session = {'organization': self.tier.organization}
        self.user = User()
        self.request.user = self.user

    @patch.object(User, 'is_authenticated', PropertyMock(return_value=True))
    @override_settings(TIERS_EXPIRED_REDIRECT_URL='/expired')
    def test_added_session_attribs(self):
        self.middleware.process_request(self.request)
        assert self.request.session['TIER_EXPIRED']
        assert self.request.session['TIER_NAME'] == 'trial'

    @patch.object(User, 'is_authenticated', PropertyMock(return_value=True))
    @override_settings(TIERS_EXPIRED_REDIRECT_URL='/expired')
    def test_redirect(self):
        response = self.middleware.process_request(self.request)
        assert response, 'should redirect'
        assert response.status_code == 302 and response['Location'] == '/expired', 'should redirect'

    @patch.object(User, 'is_authenticated', PropertyMock(return_value=True))
    @override_settings(TIERS_EXPIRED_REDIRECT_URL='/expired')
    def test_expired_url_should_not_redirect(self):
        self.request.path = '/expired'
        response = self.middleware.process_request(self.request)
        assert not response, 'should NOT redirect if it is already on expred url'

    @patch.object(User, 'is_authenticated', PropertyMock(return_value=True))
    @override_settings(TIERS_EXPIRED_REDIRECT_URL='/expired')
    def test_admin_url_should_not_redirect(self):
        self.request.path = '/admin'
        response = self.middleware.process_request(self.request)
        assert not response, 'should NOT redirect if if on /admin'

    @patch.object(User, 'is_authenticated', PropertyMock(return_value=True))
    @override_settings(TIERS_EXPIRED_REDIRECT_URL='/expired')
    def test_homepage_url_should_redirect(self):
        self.request.path = '/'
        response = self.middleware.process_request(self.request)
        assert response, 'should redirect if if on homepage "/"'

    @patch.object(User, 'is_authenticated', PropertyMock(return_value=False))
    def test_default_session_attribs_for_non_authenticated(self):
        self.middleware.process_request(self.request)
        assert 'TIER_NAME' not in self.request.session

    @patch.object(User, 'is_authenticated', PropertyMock(return_value=False))
    @override_switch(REDIRECT_NON_AUTHENTICATED, active=True)
    def test_redirect_non_authenticated(self):
        self.middleware.process_request(self.request)
        assert 'TIER_NAME' in self.request.session
        assert self.request.session['TIER_EXPIRED']
