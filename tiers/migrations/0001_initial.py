# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.utils.timezone
import model_utils.fields
import tiers.models

from ..app_settings import ORGANIZATION_MODEL


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(ORGANIZATION_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(default=b'trial', max_length=255, choices=[(b'trial', b'Trial')])),
                ('tier_enforcement_exempt', models.BooleanField(default=False)),
                ('tier_enforcement_grace_period', models.PositiveIntegerField(default=14)),
                ('tier_expires_at', models.DateTimeField(default=tiers.models.set_default_expiration)),
                ('organization', models.OneToOneField(related_name='tier', to=ORGANIZATION_MODEL, on_delete=models.deletion.DO_NOTHING)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
