# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0025_auto_20150306_1957'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meetup',
            old_name='type',
            new_name='meetup_type',
        ),
        migrations.AddField(
            model_name='job',
            name='website',
            field=models.URLField(help_text=b'Link to your offer or company website.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='meetup',
            name='website',
            field=models.URLField(help_text=b'Link to your meetup or organisation website.', null=True, blank=True),
            preserve_default=True,
        ),
    ]
