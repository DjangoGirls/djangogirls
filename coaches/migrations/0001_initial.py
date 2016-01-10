# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0011_auto_20150814_0439'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('answer', models.TextField()),
            ],
            options={
                'ordering': ('question__order',),
            },
        ),
        migrations.CreateModel(
            name='CoachApplication',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('number', models.PositiveIntegerField(default=1, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('state', models.CharField(choices=[('submitted', 'Coach form submitted'), ('accepted', 'Registration accepted'), ('rejected', 'Registration rejected')], null=True, max_length=50, default='submitted', verbose_name='State of the coach application')),
                ('email', models.EmailField(null=True, max_length=254, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CoachEmail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('text', models.TextField(help_text='You can use HTML syntax in this message. Preview on the right.', verbose_name='Content of the email')),
                ('recipients_group', models.CharField(choices=[('submitted', 'Coach form submitted'), ('accepted', 'Registration accepted'), ('rejected', 'Registration rejected')], max_length=50, help_text='Only people assigned to chosen group will receive this email.', verbose_name='Recipients')),
                ('number_of_recipients', models.IntegerField(null=True, default=0)),
                ('successfully_sent', models.TextField(null=True, blank=True)),
                ('failed_to_sent', models.TextField(null=True, blank=True)),
                ('sent_from', models.EmailField(max_length=254)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('sent', models.DateTimeField(null=True, blank=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='email_author')),
            ],
        ),
        migrations.CreateModel(
            name='CoachForm',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('text_header', models.CharField(max_length=255, default='Register to be a coach at Django Girls [City]!')),
                ('text_description', models.TextField(default='First of all: if you\'re reading this, that means you\'ve decided to help us out during Django Girls workshop. You rock! Thank you :) \n\nWe\'re doing this quick survey to gather all the information about coaches in one place, to get to know you better and make sure we can find a group of learners who will be the best match for you.\n\nYou can find the coaching manual <a href="http://coach.djangogirls.org/">here</a>.')),
                ('confirmation_mail', models.TextField(help_text='Mail will be sent from your event mail.\nAlso the answers will be attached.', default='Hi there!This is a confirmation of your registering to coach at <a href="http://djangogirls.org/{city}">Django Girls {CITY}</a>. Yay! Thank you so much!\n\nYou\'ll receive an email from the team that organizes Django Girls {CITY} soon. You can always reach them by answering to this email or by writing to {your event mail}.\nFor your reference, we\'re attaching your answers below.\n\nHugs, rainbows and sparkles!\nDjango Girls')),
                ('open_from', models.DateTimeField(null=True, verbose_name='Coach application process is open from')),
                ('open_until', models.DateTimeField(null=True, verbose_name='Coach application process is open until')),
                ('page', models.ForeignKey(to='core.EventPage')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.TextField(verbose_name='Question')),
                ('help_text', models.TextField(default='', verbose_name='Additional help text to the question?', blank=True)),
                ('question_type', models.CharField(choices=[('paragraph', 'Paragraph'), ('text', 'Long text'), ('choices', 'Choices'), ('email', 'Email')], max_length=50, verbose_name='Type of the question')),
                ('is_required', models.BooleanField(default=True, verbose_name='Is the answer to the question required?')),
                ('choices', models.TextField(help_text="Used only with 'Choices' question type", default='', verbose_name='List all available options, separated with semicolon (;)', blank=True)),
                ('is_multiple_choice', models.BooleanField(help_text="Used only with 'Choices' question type", default=False, verbose_name='Are there multiple choices allowed?')),
                ('order', models.PositiveIntegerField(help_text='Position of the question')),
                ('form', models.ForeignKey(to='coaches.CoachForm')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='coachemail',
            name='form',
            field=models.ForeignKey(to='coaches.CoachForm'),
        ),
        migrations.AddField(
            model_name='coachapplication',
            name='form',
            field=models.ForeignKey(to='coaches.CoachForm'),
        ),
        migrations.AddField(
            model_name='answer',
            name='application',
            field=models.ForeignKey(to='coaches.CoachApplication'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='coaches.Question'),
        ),
    ]
