# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.core.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('applications', '0004_auto_20150322_1050'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField(blank=True, help_text=b'5 being the most positive, 1 being the most negative.', null=True, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('comment', models.TextField(help_text=b'Any extra comments?', null=True, blank=True)),
                ('application', models.ForeignKey(related_name=b'scores', to='applications.Application')),
                ('user', models.ForeignKey(related_name=b'scores', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='score',
            unique_together=set([('user', 'application')]),
        ),
    ]
