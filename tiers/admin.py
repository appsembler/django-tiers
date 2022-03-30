# -*- coding: utf-8 -*-


from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from django.utils import timezone

from .models import Tier


def make_exempt(modeladmin, request, queryset):
    queryset.update(tier_enforcement_exempt=True)


make_exempt.short_description = "Exempt from tier enforcement"


class ActiveTierFilter(SimpleListFilter):
    """
    Admin filter for tier active/inactive status.

    TODO: Add support for graceperiod
    """

    title = 'Tier status'
    parameter_name = 'tier_status'

    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'

    def lookups(self, request, model_admin):
        return [
            [self.STATUS_ACTIVE, 'Active Tiers'],
            [self.STATUS_INACTIVE, 'Inactive Tiers'],
        ]

    def queryset(self, request, queryset):
        active_tiers_filter = Q(tier_enforcement_exempt=True) | Q(tier_expires_at__gte=timezone.now())
        if self.value() == self.STATUS_ACTIVE:
            queryset = queryset.filter(active_tiers_filter)
        elif self.value() == self.STATUS_INACTIVE:
            queryset = queryset.exclude(active_tiers_filter)
        return queryset


class TierAdmin(admin.ModelAdmin):
    list_display = ('organization', 'get_microsites', 'name', 'tier_expires_at', 'tier_enforcement_exempt',)
    search_fields = ['organization__name', 'name']
    list_filter = ['name', ActiveTierFilter, 'tier_expires_at', 'tier_enforcement_exempt']
    actions = [make_exempt]

    def get_microsites(self, obj):
        return "\n".join(obj.organization.microsites.values_list('subdomain', flat=True))
    get_microsites.short_description = 'Microsite'
    get_microsites.admin_order_field = 'organization__microsites__subdomain'


admin.site.register(Tier, TierAdmin)
