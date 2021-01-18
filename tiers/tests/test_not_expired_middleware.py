from __future__ import unicode_literals

import pytest

from datetime import datetime, timedelta
from mock import patch, Mock, PropertyMock

from django.contrib.auth.models import User

from tiers.tests.factories import TierFactory, tiers_request_factory
from tiers.middleware import TierMiddleware


pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize('attrib', [
    'DISPLAY_EXPIRATION_WARNING',
    'TIER_EXPIRES_IN',
    'TIER_EXPIRED',
    'TIER_NAME',
])
def test_empty_by_default_attributes(attrib):
    """
    Test that the tiers attributes are not added by default.
    """
    default = object()
    tiers_request = tiers_request_factory()
    assert tiers_request.session.get(attrib, default) is default


@patch('tiers.middleware.reverse', Mock(return_value='/something'))
def test_added_session_attribs():
    """
    Test the session attribute that are added by the middleware.
    """
    middleware = TierMiddleware()
    tier = TierFactory.create(tier_expires_at=datetime.now() + timedelta(days=40))
    tiers_request = tiers_request_factory(tier.organization)
    with patch.object(User, 'is_authenticated', PropertyMock(return_value=True)):
        middleware.process_request(tiers_request)
    assert not tiers_request.session['TIER_EXPIRED']
    assert tiers_request.session['TIER_EXPIRES_IN'] == tier.time_til_tier_expires()
    assert tiers_request.session['DISPLAY_EXPIRATION_WARNING']
    assert tiers_request.session['TIER_NAME'] == 'trial'
