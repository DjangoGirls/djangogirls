# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0028_auto_20150311_0701'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='ready_to_publish',
        ),
        migrations.RemoveField(
            model_name='meetup',
            name='ready_to_publish',
        ),
        migrations.AlterField(
            model_name='job',
            name='review_status',
            field=models.CharField(default=b'OPN', max_length=3, choices=[(b'OPN', b'Open'), (b'URE', b'Under review'), (b'RTP', b'Ready to publish'), (b'PUB', b'Published'), (b'EXP', b'Expired')]),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='meetup_date',
            field=models.DateTimeField(help_text=b'If this is a recurring meetup/event, please enter a start date.            Date format: YYYY-MM-DD', null=True),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='review_status',
            field=models.CharField(default=b'OPN', max_length=3, choices=[(b'OPN', b'Open'), (b'URE', b'Under review'), (b'RTP', b'Ready to publish'), (b'PUB', b'Published'), (b'EXP', b'Expired')]),
        ),
    ]
