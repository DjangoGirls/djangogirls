# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0013_auto_20150119_1904'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='job',
            options={'ordering': ['-published_date']},
        ),
        migrations.RenameField(
            model_name='job',
            old_name='post_date',
            new_name='published_date',
        ),
        migrations.AlterField(
            model_name='job',
            name='reviewer',
            field=models.ForeignKey(related_name=b'jobs', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
