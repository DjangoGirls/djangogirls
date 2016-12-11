# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0005_auto_20150322_1439'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ('question__order',)},
        ),
        migrations.AddField(
            model_name='application',
            name='email',
            field=models.EmailField(max_length=75, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='application',
            name='newsletter_optin',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='application',
            name='state',
            field=models.CharField(max_length=50, null=True, verbose_name=b'State of the application', choices=[(b'submitted', b'Submitted'), (b'accepted', b'Accepted'), (b'rejected', b'Rejected'), (b'waitlisted', b'Waiting list')]),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(max_length=50, verbose_name=b'Type of the question', choices=[(b'paragraph', b'Paragraph'), (b'text', b'Long text'), (b'choices', b'Choices'), (b'email', b'Email')]),
        ),
    ]
