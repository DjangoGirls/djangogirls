# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_contactemail'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactemail',
            name='contact_type',
            field=models.CharField(choices=[('chapter', 'Djangogirls Chapter'), ('support', 'Djangogirls Support team')], default='chapter', max_length=20),
        ),
        migrations.AddField(
            model_name='contactemail',
            name='event',
            field=models.ForeignKey(blank=True, null=True, to='core.Event'),
        ),
        migrations.AddField(
            model_name='contactemail',
            name='sent_successfully',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='contactemail',
            name='email',
            field=models.EmailField(max_length=128),
        ),
        migrations.AlterField(
            model_name='contactemail',
            name='sent_to',
            field=models.EmailField(max_length=128),
        ),
    ]
