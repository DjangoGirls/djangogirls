# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0006_auto_20150116_1737'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ['name'], 'verbose_name': 'Company', 'verbose_name_plural': 'Companies'},
        ),
        migrations.AddField(
            model_name='job',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job',
            name='published',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='job',
            name='post_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
