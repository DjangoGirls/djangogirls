# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20151203_1109'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactEmail',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=128)),
                ('email', models.CharField(max_length=128)),
                ('sent_to', models.CharField(max_length=128)),
                ('message', models.TextField()),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]
