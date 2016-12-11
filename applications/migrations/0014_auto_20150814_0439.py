# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0013_auto_20150624_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='rsvp_status',
            field=models.CharField(choices=[('waiting', 'RSVP: Waiting for response'), ('yes', 'RSVP: Confirmed attendance'), ('no', 'RSVP: Rejected invitation')], default='waiting', max_length=50, verbose_name='RSVP status'),
        ),
        migrations.AlterField(
            model_name='application',
            name='state',
            field=models.CharField(choices=[('submitted', 'Application submitted'), ('accepted', 'Application accepted'), ('rejected', 'Application rejected'), ('waitlisted', 'Application on waiting list')], default='submitted', max_length=50, verbose_name='State of the application', null=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='recipients_group',
            field=models.CharField(choices=[('submitted', 'Application submitted'), ('accepted', 'Application accepted'), ('rejected', 'Application rejected'), ('waitlisted', 'Application on waiting list'), ('waiting', 'RSVP: Waiting for response'), ('yes', 'RSVP: Confirmed attendance'), ('no', 'RSVP: Rejected invitation')], max_length=50, verbose_name='Recipients', help_text='Only people assigned to chosen group will receive this email.'),
        ),
        migrations.AlterField(
            model_name='email',
            name='text',
            field=models.TextField(verbose_name='Content of the email', help_text='You can use HTML syntax in this message. Preview on the right.'),
        ),
        migrations.AlterField(
            model_name='form',
            name='confirmation_mail',
            field=models.TextField(default='Hi there!This is a confirmation of your application to <a href="http://djangogirls.org/{city}">Django Girls {CITY}</a>. Yay! That\'s a huge step already, we\'re proud of you!\n\nMind that this is not a confirmation of participation in the event, but a confirmation that we received your application.\n\nYou\'ll receive an email from the team that organizes Django Girls {CITY} soon. You can always reach them by answering to this email or by writing to {your event mail}.\nFor your reference, we\'re attaching your answers below.\n\nHugs, cupcakes and high-fives!\nDjango Girls', help_text='Mail will be sent from your event mail.\nAlso the answers will be attached.'),
        ),
        migrations.AlterField(
            model_name='form',
            name='open_from',
            field=models.DateTimeField(verbose_name='Application process is open from', null=True),
        ),
        migrations.AlterField(
            model_name='form',
            name='open_until',
            field=models.DateTimeField(verbose_name='Application process is open until', null=True),
        ),
        migrations.AlterField(
            model_name='form',
            name='text_description',
            field=models.TextField(default="Yay! We're so excited you want to be a part of our workshop. Please mind that filling out the form below does not give you a place on the workshop, but a chance to get one. The application process is open from {INSERT DATE} until {INSERT DATE}. If you're curious about the criteria we use to choose applicants, you can read about it on <a href='http://blog.djangogirls.org/post/91067112853/djangogirls-how-we-scored-applications'>Django Girls blog</a>. Good luck!"),
        ),
        migrations.AlterField(
            model_name='form',
            name='text_header',
            field=models.CharField(default='Apply for a spot at Django Girls [City]!', max_length=255),
        ),
        migrations.AlterField(
            model_name='question',
            name='choices',
            field=models.TextField(default='', verbose_name='List all available options, separated with semicolon (;)', blank=True, help_text="Used only with 'Choices' question type"),
        ),
        migrations.AlterField(
            model_name='question',
            name='help_text',
            field=models.TextField(default='', verbose_name='Additional help text to the question?', blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='is_multiple_choice',
            field=models.BooleanField(default=False, verbose_name='Are there multiple choices allowed?', help_text="Used only with 'Choices' question type"),
        ),
        migrations.AlterField(
            model_name='question',
            name='is_required',
            field=models.BooleanField(default=True, verbose_name='Is the answer to the question required?'),
        ),
        migrations.AlterField(
            model_name='question',
            name='order',
            field=models.PositiveIntegerField(help_text='Position of the question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('paragraph', 'Paragraph'), ('text', 'Long text'), ('choices', 'Choices'), ('email', 'Email')], max_length=50, verbose_name='Type of the question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.TextField(verbose_name='Question'),
        ),
        migrations.AlterField(
            model_name='score',
            name='comment',
            field=models.TextField(null=True, blank=True, help_text='Any extra comments?'),
        ),
        migrations.AlterField(
            model_name='score',
            name='score',
            field=models.FloatField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)], help_text='5 being the most positive, 1 being the most negative.'),
        ),
    ]
