# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0023_auto_20150303_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetup',
            name='is_recurring',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='meetup_date',
            field=models.DateTimeField(help_text=b'If this is a recurring meetup/event, please enter a start date.            Date format: DD-MM-YYYY', null=True),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='organisation',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='recurrence',
            field=models.CharField(help_text=b'Provide details of recurrence if applicable.', max_length=255, null=True, blank=True),
        ),
    ]
