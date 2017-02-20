from datetime import datetime, timedelta

import pytest

from tiers.tests.utils import TiersTestCaseBase
from tiers.tests.factories import OrganizationFactory, TierFactory


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

