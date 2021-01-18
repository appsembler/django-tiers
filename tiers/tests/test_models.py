from __future__ import unicode_literals

import pytest
import re

from datetime import datetime, timedelta

from tiers.tests.factories import TierFactory


pytestmark = [pytest.mark.django_db]


def test_non_expired_tier():
    t = TierFactory()
    assert t.tier_enforcement_exempt is False
    assert t.has_tier_expired() is False
    assert t.has_tier_grace_period_expired() is False


def test_expired_tier():
    t = TierFactory(tier_expires_at=(datetime.now() - timedelta(days=2)))
    assert t.tier_enforcement_exempt is False
    assert t.has_tier_expired() is True
    assert t.has_tier_grace_period_expired() is False


def test_expired_grade_period():
    t = TierFactory(tier_expires_at=(datetime.now() - timedelta(days=20)))
    assert t.tier_enforcement_exempt is False
    assert t.has_tier_expired() is True
    assert t.has_tier_grace_period_expired() is True


def test_exemption():
    t = TierFactory(
        tier_enforcement_exempt=True,
        tier_expires_at=(datetime.now() - timedelta(days=20)))
    assert t.tier_enforcement_exempt is True
    assert t.has_tier_expired() is False
    assert t.has_tier_grace_period_expired() is False


def test_expire_message():
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
