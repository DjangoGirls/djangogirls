# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0003_auto_20150311_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='state',
            field=models.CharField(max_length=50, null=True, verbose_name=b'State of the application', choices=[(b'submitted', b'Submitted'), (b'accepted', b'Accepted'), (b'rejected', b'Rejected')]),
            preserve_default=True,
        ),
    ]
