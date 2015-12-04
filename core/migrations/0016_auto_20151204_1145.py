# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20151204_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactemail',
            name='event',
            field=models.ForeignKey(blank=True, to='core.Event', help_text='required for Chapter contact', null=True),
        ),
    ]
