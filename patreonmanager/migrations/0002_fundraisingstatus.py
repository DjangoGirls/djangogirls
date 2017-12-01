# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patreonmanager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FundraisingStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('number_of_patrons', models.IntegerField()),
                ('amount_raised', models.IntegerField()),
            ],
        ),
    ]
