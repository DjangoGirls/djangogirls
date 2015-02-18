# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django_countries.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=500)),
                ('website', models.URLField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500)),
                ('contact_email', models.EmailField(max_length=254)),
                ('city', models.CharField(max_length=100)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('description', models.TextField(max_length=2000)),
                ('review_status', models.BooleanField(default=False)),
                ('reviewers_comment', models.TextField(max_length=2000, null=True, blank=True)),
                ('post_date', models.DateTimeField(auto_now_add=True)),
                ('expiration_date', models.DateTimeField()),
                ('company', models.ForeignKey(related_name=b'company', to='jobs.Company')),
                ('reviewer', models.ForeignKey(related_name=b'reviewer', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='job',
            unique_together=set([('company', 'title')]),
        ),
    ]
