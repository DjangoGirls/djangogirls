from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models
from django_date_extensions.fields import ApproximateDateField

from core.create_event import create_event_from_event_application
from core.models import Event
from core.validators import validate_approximatedate

from .constants import (
    APPLICATION_STATUS,
    INVOLVEMENT_CHOICES,
    NEW,
    ON_HOLD,
    REJECTED,
)


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
    involvement = models.CharField(choices=INVOLVEMENT_CHOICES, max_length=15)
    experience = models.TextField()
    venue = models.TextField()
    sponsorship = models.TextField()
    coaches = models.TextField()

    # status reflecting state of the event in a triaging process.
    status = models.CharField(
        choices=APPLICATION_STATUS,
        default=NEW,
        max_length=10,
    )
    status_changed_at = models.DateTimeField(null=True, blank=True)

    rejection_reason = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        permissions = (
            ("can_accept_organize_application",
             "Can accept Organize Applications"),
        )

    def accept(self):
        # create Event
        event = create_event_from_event_application(event_application=self)
        add_organizers(team, event)

        # copy organizers and add them to Event
        # set status to ACCEPTED
        # create gmail account
        # send email to organizers with gmail password
        # add organizers to slack

    def clean(self):
        if self.status == ON_HOLD and not self.comment:
            raise ValidationError({
                'comment': 'This field is required.'
            })
        if self.status == REJECTED and not self.rejection_reason:
            raise ValidationError({
                'rejection_reason': 'This field is required.'
            })


class Coorganizer(models.Model):
    event_application = models.ForeignKey(
        EventApplication,
        related_name="coorganizers")
    email = models.EmailField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Co-organizer"
        verbose_name_plural = "Co-organizers"
