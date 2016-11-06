# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0002_auto_20150308_2229'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ('form', 'order')},
        ),
        migrations.RemoveField(
            model_name='question',
            name='has_option_other',
        ),
        migrations.AlterField(
            model_name='form',
            name='text_description',
            field=models.TextField(default=b"Yay! We're so excited you want to be a part of our workshop. Please mind that filling out the form below does not give you a place on the workshop, but a chance to get one. The application process is open from {INSERT DATE} until {INSERT DATE}. If you're curious about the criteria we use to choose applicants, you can read about it on <a href='http://blog.djangogirls.org/post/91067112853/djangogirls-how-we-scored-applications'>Django Girls blog</a>. Good luck!"),
        ),
    ]
