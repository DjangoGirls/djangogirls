# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_contactemail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactemail',
            name='contact_type',
            field=models.CharField(default='chapter', max_length=20, choices=[('chapter', 'Django Girls Chapter'), ('support', 'Django Girls HQ (Support Team)')], verbose_name='Who do you want to contact?'),
        ),
        migrations.AlterField(
            model_name='contactemail',
            name='event',
            field=models.ForeignKey(help_text='required for contacting a chapter', to='core.Event', blank=True, null=True),
        ),
    ]
