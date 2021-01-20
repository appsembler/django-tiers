# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from ..app_settings import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tiers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tier',
            name='name',
            field=models.CharField(default=b'trial', max_length=255, choices=[(b'trial', b'Trial'), (b'basic', b'Basic')]),
        ),
        migrations.AlterField(
            model_name='tier',
            name='organization',
            field=models.OneToOneField(related_name='tier', null=True, blank=True, to=settings.organization_model(), on_delete=models.deletion.DO_NOTHING),
        ),
    ]
