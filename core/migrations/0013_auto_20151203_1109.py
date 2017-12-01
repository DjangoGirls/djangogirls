# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpagecontent',
            name='page',
            field=models.ForeignKey(to='core.EventPage', related_name='content'),
        ),
        migrations.AlterField(
            model_name='eventpagemenu',
            name='page',
            field=models.ForeignKey(to='core.EventPage', related_name='menu'),
        ),
    ]
