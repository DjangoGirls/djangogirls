# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0026_auto_20150306_2003'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='job',
            options={'ordering': ['-published_date']},
        ),
        migrations.AlterModelOptions(
            name='meetup',
            options={'ordering': ['-published_date']},
        ),
        migrations.AlterField(
            model_name='job',
            name='reviewer',
            field=models.ForeignKey(related_name=b'jobs_job_related', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='reviewer',
            field=models.ForeignKey(related_name=b'jobs_meetup_related', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
