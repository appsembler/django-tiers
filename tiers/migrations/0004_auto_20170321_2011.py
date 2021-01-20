# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion

from ..app_settings import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tiers', '0003_auto_20170321_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tier',
            name='organization',
            field=models.OneToOneField(related_name='tier', null=True, on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to=settings.organization_model()),
        ),
    ]
