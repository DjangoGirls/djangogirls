# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0010_auto_20150608_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='rsvp_no_code',
            field=models.CharField(max_length=24, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='rsvp_status',
            field=models.CharField(default=b'waiting', max_length=50, verbose_name=b'RSVP status', choices=[(b'waiting', b'Waiting for response'), (b'yes', b'Confirmed attendance'), (b'no', b'Rejected invitation')]),
        ),
        migrations.AddField(
            model_name='application',
            name='rsvp_yes_code',
            field=models.CharField(max_length=24, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='state',
            field=models.CharField(default=b'submitted', max_length=50, null=True, verbose_name=b'State of the application', choices=[(b'submitted', b'Application submitted'), (b'accepted', b'Application accepted'), (b'rejected', b'Application rejected'), (b'waitlisted', b'Application on waiting list')]),
        ),
        migrations.AlterField(
            model_name='email',
            name='recipients_group',
            field=models.CharField(help_text=b'Only people assigned to chosen group will receive this email.', max_length=50, verbose_name=b'Recipients', choices=[(b'submitted', b'Application submitted'), (b'accepted', b'Application accepted'), (b'rejected', b'Application rejected'), (b'waitlisted', b'Application on waiting list')]),
        ),
        migrations.AlterField(
            model_name='email',
            name='text',
            field=models.TextField(help_text=b'You can use HTML syntax in this message. Preview on the right.', verbose_name=b'Content of the email'),
        ),
    ]
