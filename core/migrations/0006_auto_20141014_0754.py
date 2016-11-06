# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_story'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('twitter_handle', models.CharField(help_text=b'No @, No http://, just username', max_length=200, null=True, blank=True)),
                ('photo', models.ImageField(help_text=b'For best display keep it square', null=True, upload_to=b'event/coaches/', blank=True)),
                ('url', models.URLField(null=True, blank=True)),
                ('event_page_content', models.ForeignKey(to='core.EventPageContent')),
            ],
            options={
                'ordering': ('?',),
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='story',
            name='created',
            field=models.DateField(auto_now_add=True),
        ),
    ]
