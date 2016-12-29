# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.utils.timezone
import django_date_extensions.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('email', models.EmailField(unique=True, max_length=75)),
                ('first_name', models.CharField(max_length=30, blank=True)),
                ('last_name', models.CharField(max_length=30, blank=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(verbose_name='groups', to='auth.Group', blank=True, related_name='user_set', related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.')),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', to='auth.Permission', blank=True, related_name='user_set', related_query_name='user', help_text='Specific permissions for this user.')),
            ],
            options={
                'verbose_name': 'Organizer',
                'verbose_name_plural': 'Organizers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('date', django_date_extensions.fields.ApproximateDateField(max_length=10, blank=True, null=True)),
                ('city', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=200)),
                ('latlng', models.CharField(max_length=30, blank=True, null=True)),
                ('is_on_homepage', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'List of events',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventPage',
            fields=[
                ('event', models.OneToOneField(to='core.Event', serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=200, blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True, default='Django Girls is a one-day workshop about programming in Python and Django tailored for women.')),
                ('main_color', models.CharField(max_length=6, default='FF9400', blank=True, null=True, help_text='Main color of the chapter in HEX')),
                ('custom_css', models.TextField(blank=True, null=True)),
                ('url', models.CharField(max_length=200, blank=True, null=True)),
                ('is_live', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Website',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventPageContent',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('content', models.TextField(help_text='HTML allowed')),
                ('background', models.ImageField(upload_to='event/backgrounds/', blank=True, null=True, help_text='Optional background photo')),
                ('position', models.PositiveIntegerField(help_text='Position of the block on the website')),
                ('is_public', models.BooleanField(default=False)),
                ('page', models.ForeignKey(to='core.EventPage')),
            ],
            options={
                'ordering': ('position',),
                'verbose_name': 'Website Content',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventPageMenu',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('position', models.PositiveIntegerField(help_text='Order of menu')),
                ('page', models.ForeignKey(to='core.EventPage')),
            ],
            options={
                'ordering': ('position',),
                'verbose_name': 'Website Menu',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200, blank=True, null=True)),
                ('logo', models.ImageField(upload_to='event/sponsors/', blank=True, null=True, help_text='Make sure logo is not bigger than 200 pixels wide')),
                ('url', models.URLField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('position', models.PositiveIntegerField(help_text='Position of the sponsor')),
                ('event_page_content', models.ForeignKey(to='core.EventPageContent')),
            ],
            options={
                'ordering': ('position',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='main_organizer',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='main_organizer', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='team',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True, null=True),
            preserve_default=True,
        ),
    ]
