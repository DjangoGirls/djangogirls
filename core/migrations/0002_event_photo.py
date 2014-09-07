# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='photo',
            field=models.ImageField(null=True, upload_to=b'event/cities/', blank=True),
            preserve_default=True,
        ),
    ]
