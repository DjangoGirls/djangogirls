# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_data(apps, schema_editor):
    Sponsor = apps.get_model("core", "Sponsor")
    Coach = apps.get_model("core", "Coach")

    # Updating sponsors
    for sponsor in Sponsor.objects.all():
        sponsor.event_page_content.sponsors.add(sponsor)

    # Updating coaches
    for coach in Coach.objects.all():
        coach.event_page_content.coaches.add(coach)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20150605_0921'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpagecontent',
            name='coaches',
            field=models.ManyToManyField(to='core.Coach', verbose_name='Coaches'),
        ),
        migrations.AddField(
            model_name='eventpagecontent',
            name='sponsors',
            field=models.ManyToManyField(to='core.Sponsor', verbose_name='Sponsors'),
        ),
        migrations.RunPython(
            migrate_data,
        ),
    ]
