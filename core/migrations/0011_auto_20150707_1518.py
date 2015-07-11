# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coach',
            name='photo',
            field=models.ImageField(blank=True, upload_to='event/coaches/', null=True, help_text='For best display keep it square'),
        ),
        migrations.AlterField(
            model_name='coach',
            name='twitter_handle',
            field=models.CharField(blank=True, max_length=200, null=True, help_text='No @, No http://, just username'),
        ),
        migrations.AlterField(
            model_name='event',
            name='photo',
            field=models.ImageField(blank=True, upload_to='event/cities/', null=True, help_text='The best would be 356 x 210px'),
        ),
        migrations.AlterField(
            model_name='eventpagemenu',
            name='url',
            field=models.CharField(max_length=255, help_text='http://djangogirls.org/city/<the value you enter here>'),
        ),
        migrations.AlterField(
            model_name='postmortem',
            name='applicants_count',
            field=models.IntegerField(verbose_name='Number of applicants'),
        ),
        migrations.AlterField(
            model_name='postmortem',
            name='attendees_count',
            field=models.IntegerField(verbose_name='Number of attendees'),
        ),
        migrations.AlterField(
            model_name='postmortem',
            name='comments',
            field=models.TextField(blank=True, verbose_name='Anything else you want to share with us?', null=True),
        ),
        migrations.AlterField(
            model_name='postmortem',
            name='costs',
            field=models.TextField(blank=True, verbose_name='What are the total costs of the event?', null=True, help_text='We only collect this information for statistics and advice for future organizers.'),
        ),
        migrations.AlterField(
            model_name='postmortem',
            name='discovery',
            field=models.TextField(blank=True, verbose_name='What was the most important thing you discovered during the workshop?', null=True),
        ),
        migrations.AlterField(
            model_name='postmortem',
            name='feedback',
            field=models.TextField(blank=True, verbose_name='How we can make DjangoGirls better?', null=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='image',
            field=models.ImageField(upload_to='stories/'),
        ),
    ]
