# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0024_auto_20150306_0815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='company',
            field=models.CharField(max_length=255),
        ),
        migrations.DeleteModel(
            name='Company',
        ),
        migrations.AlterField(
            model_name='meetup',
            name='meetup_date',
            field=models.DateTimeField(help_text=b'If this is a recurring meetup/event, please enter a start date.            Date format: DD/MM/YYYY', null=True),
        ),
    ]
