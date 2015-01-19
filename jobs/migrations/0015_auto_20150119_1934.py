# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0014_auto_20150119_1918'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='published',
            new_name='ready_to_publish',
        ),
    ]
