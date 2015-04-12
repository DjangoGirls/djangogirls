# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0029_auto_20150326_1320'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='city',
            new_name='cities',
        ),
        migrations.RenameField(
            model_name='meetup',
            old_name='meetup_date',
            new_name='meetup_start_date',
        ),
        migrations.AddField(
            model_name='job',
            name='relocation',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='remote_work',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meetup',
            name='meetup_end_date',
            field=models.DateTimeField(help_text=b'Date format: YYYY-MM-DD', null=True, blank=True),
            preserve_default=True,
        ),
    ]
