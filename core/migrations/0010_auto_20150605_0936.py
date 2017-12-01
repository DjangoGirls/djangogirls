# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20150605_0922'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coach',
            name='event_page_content',
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='event_page_content',
        ),
    ]
