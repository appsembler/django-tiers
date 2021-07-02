from datetime import timedelta
from unittest.mock import Mock

from django.utils import timezone
from tiers.models import Tier
from tiers.tests.factories import TierFactory
from tiers.admin import ActiveTierFilter


def test_active_tier_filter_lookup_choices():
    filter = ActiveTierFilter(Mock(), {}, Mock(), Mock())
    assert filter.lookups(Mock(), Mock()) == [
        ['active', 'Active Tiers'],
        ['inactive', 'Inactive Tiers'],
    ]


def test_active_tier_filter_queryset(db):
    past_date = timezone.now() - timedelta(days=100)
    future_date = timezone.now() + timedelta(days=100)
    expired_inactive_tier = TierFactory.create(tier_enforcement_exempt=False, tier_expires_at=past_date)
    exempted_active_tier = TierFactory.create(tier_enforcement_exempt=True, tier_expires_at=past_date)
    active_tier = TierFactory.create(tier_enforcement_exempt=True, tier_expires_at=future_date)
    tiers = Tier.objects.all()

    active_filter = ActiveTierFilter(Mock(), {'tier_status': 'active'}, Mock(), Mock())
    assert active_tier in active_filter.queryset(Mock(), tiers), 'Should only return active tiers'
    assert exempted_active_tier in active_filter.queryset(Mock(), tiers), 'Should only return active tiers'
    assert expired_inactive_tier not in active_filter.queryset(Mock(), tiers), 'Should only return active tiers'

    inactive_filter = ActiveTierFilter(Mock(), {'tier_status': 'inactive'}, Mock(), Mock())
    assert active_tier not in inactive_filter.queryset(Mock(), tiers), 'Should only return inactive tiers'
    assert exempted_active_tier not in inactive_filter.queryset(Mock(), tiers), 'Should only return inactive tiers'
    assert expired_inactive_tier in inactive_filter.queryset(Mock(), tiers), 'Should only return inactive tiers'

    all_filter = ActiveTierFilter(Mock(), {}, Mock(), Mock())
    assert len(all_filter.queryset(Mock(), tiers)) == 3, 'Should return all tiers'
