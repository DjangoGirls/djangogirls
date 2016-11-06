# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20150608_1958'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='event_mail',
            new_name='email',
        ),
    ]
