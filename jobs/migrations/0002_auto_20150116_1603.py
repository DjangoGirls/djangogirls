# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ['name'], 'verbose_name': 'Company', 'verbose_name_plural': 'Companies'},
        ),
        migrations.AlterModelOptions(
            name='job',
            options={'ordering': ['post_date']},
        ),
        migrations.AlterField(
            model_name='job',
            name='description',
            field=models.TextField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='job',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 16, 16, 3, 7, 41280)),
        ),
        migrations.AlterField(
            model_name='job',
            name='review_status',
            field=models.BooleanField(default=False, help_text=b'Check if reviewed'),
        ),
        migrations.AlterField(
            model_name='job',
            name='reviewers_comment',
            field=models.TextField(max_length=5000, null=True, blank=True),
        ),
    ]
