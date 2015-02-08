# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0018_auto_20150208_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetup',
            name='is_recurring',
            field=models.BooleanField(default=False, help_text=b'Is your meetup recurring?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meetup',
            name='meetup_date',
            field=models.DateTimeField(help_text=b'This stands for a starting date if the meetup is recurring', null=True),
            preserve_default=True,
        ),
    ]
