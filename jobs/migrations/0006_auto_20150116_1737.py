# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_auto_20150116_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='reviewer',
            field=models.ForeignKey(related_name=b'reviewer', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
