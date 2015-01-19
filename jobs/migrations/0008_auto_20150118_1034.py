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
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 17, 10, 34, 9, 398157), null=True, blank=True),
        ),
    ]
