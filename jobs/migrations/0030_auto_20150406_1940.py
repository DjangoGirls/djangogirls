# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0029_auto_20150404_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='review_status',
            field=models.CharField(default=b'OPN', max_length=3, choices=[(b'OPN', b'Open'), (b'URE', b'Under review'), (b'RTP', b'Ready to publish'), (b'REG', b'Rejected'), (b'PUB', b'Published'), (b'EXP', b'Expired')]),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='review_status',
            field=models.CharField(default=b'OPN', max_length=3, choices=[(b'OPN', b'Open'), (b'URE', b'Under review'), (b'RTP', b'Ready to publish'), (b'REG', b'Rejected'), (b'PUB', b'Published'), (b'EXP', b'Expired')]),
        ),
    ]
