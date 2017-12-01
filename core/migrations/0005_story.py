# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_event_photo_credit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('post_url', models.URLField()),
                ('image', models.ImageField(upload_to=b'stories/')),
                ('created', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
