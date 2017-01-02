# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def create_reviewer_group(apps, schema_editor, with_create_permissions=True):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    try:
        perm1 = Permission.objects.get(
            codename='change_job', content_type__app_label='jobs')
        perm2 = Permission.objects.get(
            codename='change_meetup', content_type__app_label='jobs')
    except Permission.DoesNotExist:
        if with_create_permissions:
            # Manually run create_permissions
            from django.contrib.auth.management import create_permissions

            for app_config in apps.get_app_configs():
                app_config.models_module = True
                create_permissions(app_config, apps=apps, verbosity=0)
                app_config.models_module = None
            return create_reviewer_group(
                apps, schema_editor, with_create_permissions=False)
        else:
            raise
    reviewers = Group.objects.create(name="Reviewers")
    reviewers.permissions.add(perm1, perm2)


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_reviewer_group),
    ]
