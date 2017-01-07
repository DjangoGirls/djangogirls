from __future__ import unicode_literals

from django.db import models
from django_date_extensions.fields import ApproximateDateField

from core.models import Event
from core.validators import validate_approximatedate

involvement_choices = (
    ("newcomer", "I’ve never been to a Django Girls event"),
    ("attendee", "I’m a former attendee"),
    ("coach", "I’m a former coach"),
    ("organizer", "I’m a former organizer"),
    ("contributor", "I contributed to the tutorial or translations"))


class EventApplication(models.Model):
    previous_event = models.ForeignKey(Event, null=True, blank=True)
    # workshop fields
    date = ApproximateDateField(validators=[validate_approximatedate])
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    latlng = models.CharField(max_length=30, null=True, blank=True)
    website_slug = models.SlugField()
    main_organizer_email = models.EmailField()
    main_organizer_first_name = models.CharField(max_length=30)
    main_organizer_last_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    # application fields
    about_you = models.TextField()
    why = models.TextField()
    involvement = models.CharField(choices=involvement_choices, max_length=15)
    experience = models.TextField()
    venue = models.TextField()
    sponsorhip = models.TextField()
    coaches = models.TextField()

    class Meta:
        permissions = (
            ("can_accept_organize_application",
             "Can accept Organize Applications"),
        )


class Coorganizer(models.Model):
    event_request = models.ForeignKey(EventApplication, related_name="team")
    email = models.EmailField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Co-organizer"
        verbose_name_plural = "Co-organizers"
