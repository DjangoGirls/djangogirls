# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs', '0017_auto_20150202_2209'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meetup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500)),
                ('type', models.CharField(default=b'MEET', max_length=4, choices=[(b'MEET', b'meetup'), (b'CONF', b'conference'), (b'WORK', b'workshop')])),
                ('contact_email', models.EmailField(max_length=254)),
                ('city', models.CharField(max_length=100)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('description', models.TextField(max_length=5000)),
                ('review_status', models.BooleanField(default=False, help_text=b'Check if reviewed')),
                ('reviewers_comment', models.TextField(max_length=5000, null=True, blank=True)),
                ('ready_to_publish', models.BooleanField(default=False)),
                ('published_date', models.DateTimeField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('expiration_date', models.DateField(help_text=b'Automatically is set 60 days from posting. You can override this.', null=True, blank=True)),
                ('organization', models.ForeignKey(related_name=b'meetups', blank=True, to='jobs.Company', null=True)),
                ('reviewer', models.ForeignKey(related_name=b'meetups', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-published_date'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='meetup',
            unique_together=set([('title', 'city')]),
        ),
        migrations.AlterField(
            model_name='job',
            name='company',
            field=models.ForeignKey(related_name=b'jobs', to='jobs.Company'),
        ),
    ]
