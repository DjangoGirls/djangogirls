# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patron',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('twitter', models.CharField(blank=True, max_length=50, verbose_name='twitter')),
                ('address', models.TextField(blank=True, verbose_name='address')),
                ('since', models.DateTimeField(blank=True, null=True, verbose_name='patron since')),
                ('last_update', models.DateTimeField(editable=False, verbose_name='last update', default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'patron',
                'verbose_name_plural': 'patrons',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('month', models.DateField(verbose_name='month')),
                ('pledge', models.DecimalField(decimal_places=2, verbose_name='pledge', max_digits=8)),
                ('status', models.CharField(max_length=12, default='PROCESSED', verbose_name='status', choices=[('DECLINED', 'declined'), ('PROCESSED', 'processed')])),
                ('completed', models.BooleanField(verbose_name='completed', default=False)),
                ('patron', models.ForeignKey(related_name='payments', verbose_name='patron', to='patreonmanager.Patron')),
            ],
            options={
                'verbose_name': 'payment',
                'verbose_name_plural': 'payments',
            },
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('description', models.TextField(verbose_name='description')),
                ('value', models.DecimalField(decimal_places=2, verbose_name='value', max_digits=8)),
            ],
            options={
                'ordering': ['value'],
                'verbose_name': 'reward',
                'verbose_name_plural': 'rewards',
            },
        ),
        migrations.AddField(
            model_name='payment',
            name='reward',
            field=models.ForeignKey(related_name='+', verbose_name='reward', to='patreonmanager.Reward'),
        ),
        migrations.AlterUniqueTogether(
            name='payment',
            unique_together=set([('patron', 'month')]),
        ),
    ]
