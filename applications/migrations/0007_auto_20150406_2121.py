# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('applications', '0006_auto_20150406_2042'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('recipients_group', models.CharField(max_length=50, choices=[(b'submitted', b'Submitted'), (b'accepted', b'Accepted'), (b'rejected', b'Rejected'), (b'waitlisted', b'Waiting list')])),
                ('recipients_emails', models.TextField()),
                ('sent_from', models.EmailField(max_length=75)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('sent', models.DateTimeField()),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('form', models.ForeignKey(to='applications.Form')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='application',
            name='state',
            field=models.CharField(default=b'submitted', max_length=50, null=True, verbose_name=b'State of the application', choices=[(b'submitted', b'Submitted'), (b'accepted', b'Accepted'), (b'rejected', b'Rejected'), (b'waitlisted', b'Waiting list')]),
        ),
        migrations.AlterField(
            model_name='question',
            name='choices',
            field=models.TextField(help_text=b"Used only with 'Choices' question type", null=True, verbose_name=b'List all available options, comma separated', blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='help_text',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Additional help text to the question?', blank=True),
        ),
    ]
