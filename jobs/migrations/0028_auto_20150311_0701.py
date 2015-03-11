# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0027_auto_20150307_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetup',
            name='meetup_date',
            field=models.DateTimeField(help_text=b'If this is a recurring meetup/event, please enter a start date.            Date format: YYYY/MM/DD', null=True),
        ),
    ]
