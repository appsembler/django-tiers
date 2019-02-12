from __future__ import unicode_literals

import re

from datetime import datetime, timedelta
from django.utils.timezone import now as timezone_now

from freezegun import freeze_time

from tiers.tests.utils import TiersTestCaseBase
from tiers.tests.factories import TierFactory


class TiersTests(TiersTestCaseBase):

    def test_non_expired_tier(self):
        t = TierFactory()
        assert t.tier_enforcement_exempt == False
        assert t.has_tier_expired() == False
        assert t.has_tier_grace_period_expired() == False

    def test_expired_tier(self):
        t = TierFactory(tier_expires_at=(datetime.now() - timedelta(days=2)))
        assert t.tier_enforcement_exempt == False
        assert t.has_tier_expired() == True
        assert t.has_tier_grace_period_expired() == False

    def test_expired_grade_period(self):
        t = TierFactory(tier_expires_at=(datetime.now() - timedelta(days=20)))
        assert t.tier_enforcement_exempt == False
        assert t.has_tier_expired() == True
        assert t.has_tier_grace_period_expired() == True

    def test_exemption(self):
        t = TierFactory(
            tier_enforcement_exempt=True,
            tier_expires_at=(datetime.now() - timedelta(days=20)))
        assert t.tier_enforcement_exempt == True
        assert t.has_tier_expired() == False
        assert t.has_tier_grace_period_expired() == False

    def test_expire_message(self):
        """
        Ensures that `has_tier_grace_period_expired` works well.

        This function uses regexps match what the Django `timeuntil` returns.
        The `avoid_wrapping` function has more details in the docstring.
        """
        with freeze_time(datetime(2019, 2, 5)):
            t = TierFactory.create()
            assert datetime.now() == datetime(2019, 2, 5), 'Ensure that freeze works'
            assert timezone_now() == datetime(2019, 2, 5), 'Ensure that freeze works'
            assert t.tier_expires_at == datetime(2019, 3, 7)

        with freeze_time(datetime(2019, 2, 6)):
            message = t.time_til_tier_expires()
            assert re.match('4.*weeks,.*1.*day', message), 'Should handle long time well'

        with freeze_time(datetime(2019, 3, 4, 0, 8, 0)):
            message = t.time_til_tier_expires()
            assert re.match(r'2.*days,.*23.*hours', message), 'Should short time well'

        with freeze_time(datetime(2020, 2, 6)):
            message = t.time_til_tier_expires()
            assert re.match('0.*minutes', message), 'Should handle future time well.'
