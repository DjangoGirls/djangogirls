# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20141014_0754'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coach',
            options={'ordering': ('?',), 'verbose_name_plural': 'Coaches'},
        ),
        migrations.AddField(
            model_name='event',
            name='photo_link',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
