# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_auto_20150510_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='expiration_date',
            field=models.DateField(blank=True, null=True, help_text='Automatically is set 60 days from posting. You can override this.'),
        ),
        migrations.AlterField(
            model_name='job',
            name='review_status',
            field=models.CharField(choices=[('OPN', 'Open'), ('URE', 'Under review'), ('RTP', 'Ready to publish'), ('REJ', 'Rejected'), ('PUB', 'Published')], max_length=3, default='OPN'),
        ),
        migrations.AlterField(
            model_name='job',
            name='website',
            field=models.URLField(blank=True, null=True, help_text='Link to your offer or company website.'),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='expiration_date',
            field=models.DateField(blank=True, null=True, help_text='Automatically is set 60 days from posting. You can override this.'),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='meetup_end_date',
            field=models.DateTimeField(blank=True, null=True, help_text='Date format: YYYY-MM-DD'),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='meetup_start_date',
            field=models.DateTimeField(null=True, help_text='If this is a recurring meetup/event, please enter a start date.            Date format: YYYY-MM-DD'),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='meetup_type',
            field=models.CharField(choices=[('MEET', 'meetup'), ('CONF', 'conference'), ('WORK', 'workshop')], max_length=4, default='MEET'),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='recurrence',
            field=models.CharField(blank=True, max_length=255, null=True, help_text='Provide details of recurrence if applicable.'),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='review_status',
            field=models.CharField(choices=[('OPN', 'Open'), ('URE', 'Under review'), ('RTP', 'Ready to publish'), ('REJ', 'Rejected'), ('PUB', 'Published')], max_length=3, default='OPN'),
        ),
        migrations.AlterField(
            model_name='meetup',
            name='website',
            field=models.URLField(blank=True, null=True, help_text='Link to your meetup or organisation website.'),
        ),
    ]
