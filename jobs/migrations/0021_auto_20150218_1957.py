# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0020_auto_20150213_2144'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ['name'], 'verbose_name': 'Company/Organisation', 'verbose_name_plural': 'Companies/Organisations'},
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='job',
            name='city',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='job',
            name='contact_email',
            field=models.EmailField(max_length=255),
        ),
        migrations.AlterField(
            model_name='job',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='city',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='contact_email',
            field=models.EmailField(max_length=255),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='recurrence',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
