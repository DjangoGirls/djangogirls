# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0019_auto_20150208_1859'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ['name'], 'verbose_name': 'Company\\Organisation', 'verbose_name_plural': 'Companies\\Organisations'},
        ),
        migrations.RenameField(
            model_name='meetup',
            old_name='organization',
            new_name='organisation',
        ),
        migrations.AddField(
            model_name='meetup',
            name='recurrence',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='job',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='job',
            name='reviewers_comment',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='reviewers_comment',
            field=models.TextField(null=True, blank=True),
        ),
    ]
