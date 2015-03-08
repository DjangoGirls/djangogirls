# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20141025_1521'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text_header', models.CharField(default=b'Apply for a spot at Django Girls [City]!', max_length=255)),
                ('text_description', models.TextField(default=b"Yay! We're so excited you want to be a part of our workshop. Please mind that filling out the form below does not give you a place on the workshop, but a chance to get one. The application process is open from {open_from} until {open_until}. If you're curious about the criteria we use to choose applicants, you can read about it on <a href='http://blog.djangogirls.org/post/91067112853/djangogirls-how-we-scored-applications'>Django Girls blog</a>. Good luck!")),
                ('open_from', models.DateTimeField(null=True, verbose_name=b'Application process is open from')),
                ('open_until', models.DateTimeField(null=True, verbose_name=b'Application process is open until')),
                ('page', models.ForeignKey(to='core.EventPage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name=b'Question')),
                ('help_text', models.CharField(max_length=255, null=True, verbose_name=b'Additional help text to the question?')),
                ('question_type', models.CharField(max_length=50, verbose_name=b'Type of the question', choices=[(b'paragraph', b'Paragraph'), (b'text', b'Long text'), (b'choices', b'Choices')])),
                ('is_required', models.BooleanField(verbose_name=b'Is the answer to the question required?')),
                ('choices', models.TextField(help_text=b"Used only with 'Choices' question type", null=True, verbose_name=b'List all available options, comma separated')),
                ('has_option_other', models.BooleanField(help_text=b"Used only with 'Choices' question type", verbose_name=b"Allow for 'Other' answer?")),
                ('is_multiple_choice', models.BooleanField(help_text=b"Used only with 'Choices' question type", verbose_name=b'Are there multiple choices allowed?')),
                ('order', models.PositiveIntegerField(help_text=b'Position of the question')),
                ('form', models.ForeignKey(to='applications.Form')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='application',
            name='form',
            field=models.ForeignKey(to='applications.Form'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='application',
            field=models.ForeignKey(to='applications.Application'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='applications.Question'),
            preserve_default=True,
        ),
    ]
