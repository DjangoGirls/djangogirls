# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20151203_1122'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=128)),
                ('sent_to', models.EmailField(max_length=128)),
                ('message', models.TextField()),
                ('contact_type', models.CharField(default='chapter', choices=[('chapter', 'Djangogirls Chapter'), ('support', 'Djangogirls Support team')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sent_successfully', models.BooleanField(default=True)),
                ('event', models.ForeignKey(to='core.Event', blank=True, null=True, help_text='required for Chapter contact')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]
