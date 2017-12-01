# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0007_auto_20150406_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailmessage',
            name='recipients_emails',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='emailmessage',
            name='sent',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
