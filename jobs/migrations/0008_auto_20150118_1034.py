# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0007_auto_20150116_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='expiration_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
