from __future__ import unicode_literals

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.db import models, transaction
from django.utils import timezone
from django.template.loader import render_to_string
from django_date_extensions.fields import ApproximateDateField

from core.create_event import create_event_from_event_application
from core.create_organizers import create_organizers
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
    about_you = models.TextField("About organizer")
    why = models.TextField("Motivations to organize")
    involvement = models.CharField("Involvement in Django Girls",
                                   choices=INVOLVEMENT_CHOICES, max_length=15)
    experience = models.TextField("Experience with organizing other events")
    venue = models.TextField("Information about your potential venue")
    sponsorship = models.TextField("Information about your potential sponsorship")
    coaches = models.TextField("Information about your potential coaches")

    # status reflecting state of the event in a triaging process.
    status = models.CharField(
        choices=APPLICATION_STATUS,
        default=NEW,
        max_length=10,
    )
    status_changed_at = models.DateTimeField(null=True, blank=True)

    comment = models.TextField(null=True, blank=True)

    class Meta:
        permissions = (
            ("can_accept_organize_application",
             "Can accept Organize Applications"),
        )

    def __str__(self):
        return "{}, {} ({})".format(self.city, self.country, self.get_status_display())
    
    def deploy_event(self):
        """ Deploy Event based on the current EventApplication """
        # create Event
        event = create_event_from_event_application(event_application=self)

        # TODO: use method created in separate branch to create gmail accoout
        # and get password from it.
        create_organizers(event, event_application=self, email_password="PASS")

        # create gmail account
        # send email to organizers with gmail password
        # add organizers to slack

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

    @transaction.atomic
    def reject(self):
        """
        Rejecting event in triaging. Performs following actions:
        - changes status to REJECTED
        - sends a rejection email
        """
        if not self.status == REJECTED:
            self.status = REJECTED
            self.status_changed_at = timezone.now()
            self.save()
            self.send_rejection_email()

    def send_rejection_email(self):
        """
        Sends a rejection email to all organizars who created this application
        """
        subject = "Application to organize Django Girls {} has been reviewed".format(self.city)
        content = render_to_string('emails/organize/rejection.html', {'application': self})
        recipients = self.get_all_recipients()
        msg = EmailMessage(subject, content, settings.DEFAULT_FROM_EMAIL, recipients)
        msg.content_subtype = "html"
        msg.send()

    def send_event_deployed_email(self, event, email_password):
        """
        Sends a event deployed email to all organizers who created this application
        """
        subject = "Congrats! Your application to organize Django Girls {} has been accepted!".format(self.city)
        content = render_to_string('emails/organize/event_deployed.html', {
            'event': event,
            'password': email_password,
        })
        recipients = self.get_all_recipients()
        recipients.append(event.email)  # add event's djangogirls.org email
        msg = EmailMessage(subject, content, settings.DEFAULT_FROM_EMAIL, recipients)
        msg.content_subtype = "html"
        msg.send()


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
