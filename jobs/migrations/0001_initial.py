# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('review_status', models.CharField(default=b'OPN', max_length=3, choices=[(b'OPN', b'Open'), (b'URE', b'Under review'), (b'RTP', b'Ready to publish'), (b'REJ', b'Rejected'), (b'PUB', b'Published'), (b'EXP', b'Expired')])),
                ('reviewers_comment', models.TextField(null=True, blank=True)),
                ('published_date', models.DateTimeField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('expiration_date', models.DateField(help_text=b'Automatically is set 60 days from posting. You can override this.', null=True, blank=True)),
                ('title', models.CharField(max_length=255)),
                ('company', models.CharField(max_length=255)),
                ('website', models.URLField(help_text=b'Link to your offer or company website.', null=True, blank=True)),
                ('contact_email', models.EmailField(max_length=255)),
                ('cities', models.CharField(max_length=255)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('description', models.TextField()),
                ('remote_work', models.BooleanField(default=False)),
                ('relocation', models.BooleanField(default=False)),
                ('reviewer', models.ForeignKey(related_name=b'jobs_job_related', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-published_date'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Meetup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('review_status', models.CharField(default=b'OPN', max_length=3, choices=[(b'OPN', b'Open'), (b'URE', b'Under review'), (b'RTP', b'Ready to publish'), (b'REJ', b'Rejected'), (b'PUB', b'Published'), (b'EXP', b'Expired')])),
                ('reviewers_comment', models.TextField(null=True, blank=True)),
                ('published_date', models.DateTimeField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('expiration_date', models.DateField(help_text=b'Automatically is set 60 days from posting. You can override this.', null=True, blank=True)),
                ('title', models.CharField(max_length=255)),
                ('organisation', models.CharField(max_length=255, null=True, blank=True)),
                ('meetup_type', models.CharField(default=b'MEET', max_length=4, choices=[(b'MEET', b'meetup'), (b'CONF', b'conference'), (b'WORK', b'workshop')])),
                ('contact_email', models.EmailField(max_length=255)),
                ('website', models.URLField(help_text=b'Link to your meetup or organisation website.', null=True, blank=True)),
                ('city', models.CharField(max_length=255)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('description', models.TextField()),
                ('is_recurring', models.BooleanField(default=False)),
                ('recurrence', models.CharField(help_text=b'Provide details of recurrence if applicable.', max_length=255, null=True, blank=True)),
                ('meetup_start_date', models.DateTimeField(help_text=b'If this is a recurring meetup/event, please enter a start date.            Date format: YYYY-MM-DD', null=True)),
                ('meetup_end_date', models.DateTimeField(help_text=b'Date format: YYYY-MM-DD', null=True, blank=True)),
                ('reviewer', models.ForeignKey(related_name=b'jobs_meetup_related', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-published_date'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='meetup',
            unique_together=set([('title', 'city')]),
        ),
        migrations.AlterUniqueTogether(
            name='job',
            unique_together=set([('company', 'title')]),
        ),
    ]
