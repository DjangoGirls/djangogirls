# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20151203_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='eventpage',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
