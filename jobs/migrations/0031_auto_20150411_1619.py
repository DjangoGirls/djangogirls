# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0030_auto_20150403_1604'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meetup',
            old_name='meetup_date',
            new_name='meetup_start_date',
        ),
        migrations.AddField(
            model_name='meetup',
            name='meetup_end_date',
            field=models.DateTimeField(help_text=b'Date format: YYYY-MM-DD', null=True),
            preserve_default=True,
        ),
    ]
