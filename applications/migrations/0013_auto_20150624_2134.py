# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0012_auto_20150618_2041'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='application',
            name='number',
            field=models.PositiveIntegerField(default=1, blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='choices',
            field=models.TextField(default=b'', help_text=b"Used only with 'Choices' question type", verbose_name=b'List all available options, separated with semicolon (;)', blank=True),
        ),
    ]
