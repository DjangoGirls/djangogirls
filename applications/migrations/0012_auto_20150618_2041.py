# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0011_auto_20150614_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='choices',
            field=models.TextField(default=b'', help_text=b"Used only with 'Choices' question type", verbose_name=b'List all available options, comma separated', blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='help_text',
            field=models.TextField(default=b'', verbose_name=b'Additional help text to the question?', blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.TextField(verbose_name=b'Question'),
        ),
    ]
