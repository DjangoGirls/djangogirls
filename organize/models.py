from __future__ import unicode_literals

from autoslug import AutoSlugField
from django.core.exceptions import ValidationError
from django_countries import countries
from django.db import models, transaction
from django.utils import timezone
from django_date_extensions.fields import ApproximateDateField

from core.models import Event
from core.validators import validate_approximatedate

from .constants import (
    APPLICATION_STATUS,
    DEPLOYED,
    NEW,
    ON_HOLD,
    REJECTED,
)
from .managers import EventApplicationQuerySet
from .emails import (
    send_application_rejection_email,
    send_application_deployed_email
)


class EventApplication(models.Model):
    previous_event = models.ForeignKey(Event, null=True, blank=True)
    # workshop fields
    date = ApproximateDateField(validators=[validate_approximatedate])
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200, choices=countries)
    latlng = models.CharField(max_length=30, null=True, blank=True)
    website_slug = AutoSlugField(populate_from='city', unique=True, editable=True)
    main_organizer_email = models.EmailField()
    main_organizer_first_name = models.CharField(max_length=30)
    main_organizer_last_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    # application fields
    about_you = models.TextField("About organizer")
    why = models.TextField("Motivations to organize")
    involvement = models.CharField("Involvement in Django Girls",
                                   max_length=100)
    experience = models.TextField("Experience with organizing other events")
    venue = models.TextField("Information about your potential venue")
    sponsorship = models.TextField(
        "Information about your potential sponsorship")
    coaches = models.TextField("Information about your potential coaches")

    # status reflecting state of the event in a triaging process.
    status = models.CharField(
        choices=APPLICATION_STATUS,
        default=NEW,
        max_length=10,
    )
    status_changed_at = models.DateTimeField(null=True, blank=True)

    comment = models.TextField(null=True, blank=True)

    objects = EventApplicationQuerySet.as_manager()

    class Meta:
        permissions = (
            ("can_accept_organize_application",
             "Can accept Organize Applications"),
        )

    def __str__(self):
        return "{}, {} ({})".format(
            self.city, self.get_country_display(), self.get_status_display())

    def create_event(self):
        """ Creates event based on the data from the EventApplication.
        """
        name = 'Django Girls {}'.format(self.city)
        email = '{}@djangogirls.org'.format(self.website_slug)

        event = Event.objects.create(
            date=self.date,
            city=self.city,
            country=self.country,
            latlng=self.latlng,
            page_url=self.website_slug,
            name=name,
            page_title=name,
            email=email,
        )

        # populate content & menu from the default event
        event.add_default_content()
        event.add_default_menu()

        return event

    @transaction.atomic
    def deploy(self):
        """ Deploy Event based on the current EventApplication
            - change status to DEPLOYED
            - creates or copies event
            - add/remove organizers
            - send email about deployment
        """
        if self.status == DEPLOYED:  # we don't want to deploy twice
            return

        self.change_status_to(DEPLOYED)

        # TODO: we should recognize here if we should create a new event,
        # copy old one or copy old and change organizaers.
        event = self.create_event()

        # TODO: use method created in separate branch to create gmail acconut
        # and get password from it.
        password = "FAKE_PASS"

        # add main organizer of the Event
        main_organizer = event.add_organizer(
            self.main_organizer_email,
            self.first_name,
            self.last_name,
        )
        event.main_organizer = main_organizer
        event.save()

        # add all co-organizers
        for organizer in self.coorganizers.all():
            event.add_organizer(
                organizer.email,
                organizer.first_name,
                organizer.last_name
            )

        # TODO: remove organizers, who are no longer in org team if cloned
        send_application_deployed_email(
            event_application=self,
            event=event,
            email_password=password
        )

    def clean(self):
        if self.status == ON_HOLD and not self.comment:
            raise ValidationError({
                'comment': 'This field is required.'
            })

    def get_all_recipients(self):
        """
        Returns a list of emails to all organizers in that application
        """
        emails = [coorganizer.email for coorganizer in self.coorganizers.all()]
        emails.append(self.main_organizer_email)
        return emails

    def get_main_organizer_name(self):
        return '{} {}'.format(
            self.main_organizer_first_name,
            self.main_organizer_last_name)

    def change_status_to(self, status):
        """ Changes status to the status provided
            - sets proper status_changed_at datetime
        """
        self.status = status
        self.status_changed_at = timezone.now()
        self.save(update_fields=['status', 'status_changed_at'])

    @transaction.atomic
    def reject(self):
        """
        Rejecting event in triaging. Performs following actions:
        - changes status to REJECTED
        - sends a rejection email
        """
        if not self.status == REJECTED:
            self.change_status_to(REJECTED)
            send_application_rejection_email(event_application=self)


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
