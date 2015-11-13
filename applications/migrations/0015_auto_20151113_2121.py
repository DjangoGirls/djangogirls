# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0014_auto_20150814_0439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='state',
            field=models.CharField(choices=[('submitted', 'Application submitted'), ('accepted', 'Application accepted'), ('rejected', 'Application rejected'), ('waitlisted', 'Application on waiting list'), ('declined', 'Applicant declined')], null=True, max_length=50, default='submitted', verbose_name='State of the application'),
        ),
        migrations.AlterField(
            model_name='email',
            name='recipients_group',
            field=models.CharField(choices=[('submitted', 'Application submitted'), ('accepted', 'Application accepted'), ('rejected', 'Application rejected'), ('waitlisted', 'Application on waiting list'), ('declined', 'Applicant declined'), ('waiting', 'RSVP: Waiting for response'), ('yes', 'RSVP: Confirmed attendance'), ('no', 'RSVP: Rejected invitation')], max_length=50, help_text='Only people assigned to chosen group will receive this email.', verbose_name='Recipients'),
        ),
    ]
