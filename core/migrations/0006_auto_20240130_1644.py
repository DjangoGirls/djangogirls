# Generated by Django 3.2.20 on 2024-01-30 16:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_auto_20220422_1321"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="event",
            managers=[
                ("all_objects", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="is_blacklisted",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="OrganizerIssue",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("date_reported", models.DateField()),
                ("reported_by", models.CharField(max_length=100)),
                ("reporter_email", models.EmailField(max_length=100)),
                ("issue", models.TextField()),
                ("issue_handled", models.BooleanField()),
                ("findings", models.TextField(blank=True, null=True)),
                ("comments", models.TextField(blank=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                (
                    "event",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="event",
                        to="core.event",
                    ),
                ),
                (
                    "issue_handled_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="staff_responsible",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "organizer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="oganizer",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
