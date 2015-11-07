# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='expiration_date',
            field=models.DateField(null=True, blank=True, help_text='Enter the date until which the post should be published. By default, it is set to 60 days from posting.'),
        ),
        migrations.AlterField(
            model_name='job',
            name='internal_comment',
            field=models.TextField(null=True, blank=True, help_text="Write your comments here. They won't be sent to the company/organisation."),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='expiration_date',
            field=models.DateField(null=True, blank=True, help_text='Enter the date until which the post should be published. By default, it is set to 60 days from posting.'),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='internal_comment',
            field=models.TextField(null=True, blank=True, help_text="Write your comments here. They won't be sent to the company/organisation."),
        ),
    ]
