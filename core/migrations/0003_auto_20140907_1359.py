# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_event_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Postmortem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attendees_count', models.IntegerField(verbose_name=b'Number of attendees')),
                ('applicants_count', models.IntegerField(verbose_name=b'Number of applicants')),
                ('discovery', models.TextField(null=True, verbose_name=b'What was the most important thing you discovered during the workshop?', blank=True)),
                ('feedback', models.TextField(null=True, verbose_name=b'How we can make DjangoGirls better?', blank=True)),
                ('costs', models.TextField(help_text=b'We only collect this information for statistics and advice for future organizers.', null=True, verbose_name=b'What are the total costs of the event?', blank=True)),
                ('comments', models.TextField(null=True, verbose_name=b'Anything else you want to share with us?', blank=True)),
                ('event', models.ForeignKey(to='core.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='event',
            name='photo',
            field=models.ImageField(help_text=b'The best would be 356 x 210px', null=True, upload_to=b'event/cities/', blank=True),
        ),
    ]
