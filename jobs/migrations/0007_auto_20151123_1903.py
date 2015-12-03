# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0006_auto_20150814_0439'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='state_province',
            field=models.CharField(max_length=255, null=True, help_text='If relevant, add the name of the state or province where the job is available.', blank=True),
        ),
        migrations.AddField(
            model_name='meetup',
            name='state_province',
            field=models.CharField(max_length=255, null=True, help_text='If relevant, add the name of the state or province where the meetup/event is happening.', blank=True),
        ),
    ]
