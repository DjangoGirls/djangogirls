# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0015_auto_20150119_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='expiration_date',
            field=models.DateTimeField(help_text=b'Automatically is set 60 days from posting. You can override this.', null=True, blank=True),
        ),
    ]
