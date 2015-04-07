# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('applications', '0008_auto_20150406_2126'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=255)),
                ('text', models.TextField(help_text=b'You can use markdown syntax in this message. Preview on the right.', verbose_name=b'Content of the email')),
                ('recipients_group', models.CharField(help_text=b'Only people assigned to chosen group will receive this email.', max_length=50, verbose_name=b'Recipients', choices=[(b'submitted', b'Submitted'), (b'accepted', b'Accepted'), (b'rejected', b'Rejected'), (b'waitlisted', b'Waiting list')])),
                ('number_of_recipients', models.IntegerField(default=0, null=True)),
                ('successfuly_sent', models.TextField(null=True, blank=True)),
                ('failed_to_sent', models.TextField(null=True, blank=True)),
                ('sent_from', models.EmailField(max_length=75)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('sent', models.DateTimeField(null=True, blank=True)),
                ('author', models.ForeignKey(related_name=b'author', to=settings.AUTH_USER_MODEL)),
                ('form', models.ForeignKey(to='applications.Form')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='emailmessage',
            name='author',
        ),
        migrations.RemoveField(
            model_name='emailmessage',
            name='form',
        ),
        migrations.DeleteModel(
            name='EmailMessage',
        ),
        migrations.AddField(
            model_name='form',
            name='emails_send_from',
            field=models.EmailField(help_text=b'Which email should we use to send emails from? Use one in @djangogirls.org domain', max_length=75, null=True),
            preserve_default=True,
        ),
    ]
