# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Tier


def make_exempt(modeladmin, request, queryset):
    queryset.update(tier_enforcement_exempt=True)


make_exempt.short_description = "Exempt from tier enforcement"


class TierAdmin(admin.ModelAdmin):
    list_display = ('organization', 'get_microsites', 'name', 'tier_expires_at',
                    'tier_enforcement_grace_period', 'tier_enforcement_exempt',)
    search_fields = ['organization__name', 'name']
    list_filter = ['name', 'tier_expires_at']
    actions = [make_exempt]

    def get_microsites(self, obj):
        return "\n".join(obj.organization.microsites.values_list('subdomain', flat=True))
    get_microsites.short_description = 'Microsite'
    get_microsites.admin_order_field = 'organization__microsites__subdomain'


admin.site.register(Tier, TierAdmin)
