# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20141025_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coach',
            name='photo',
            field=models.ImageField(null=True, help_text='For best display keep it square', blank=True, upload_to='event/coaches/'),
        ),
        migrations.AlterField(
            model_name='coach',
            name='twitter_handle',
            field=models.CharField(null=True, help_text='No @, No http://, just username', blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='event',
            name='photo',
            field=models.ImageField(null=True, help_text='The best would be 356 x 210px', blank=True, upload_to='event/cities/'),
        ),
        migrations.AlterField(
            model_name='event',
            name='team',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
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
            field=models.TextField(verbose_name='Anything else you want to share with us?', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='postmortem',
            name='costs',
            field=models.TextField(verbose_name='What are the total costs of the event?', help_text='We only collect this information for statistics and advice for future organizers.', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='postmortem',
            name='discovery',
            field=models.TextField(verbose_name='What was the most important thing you discovered during the workshop?', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='postmortem',
            name='feedback',
            field=models.TextField(verbose_name='How we can make DjangoGirls better?', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='image',
            field=models.ImageField(upload_to='stories/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(verbose_name='groups', blank=True, to='auth.Group', related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(verbose_name='last login', blank=True, null=True),
        ),
    ]
