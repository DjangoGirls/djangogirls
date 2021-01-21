from django.core.exceptions import ValidationError
from django_countries import countries
from django_extensions.db.fields import AutoSlugField
from django.db import models, transaction
from django.utils import timezone
from django_date_extensions.fields import ApproximateDateField

from core import gmail_accounts
from core.deploy_event import copy_event
from core.models import Event
from core.validators import validate_approximatedate
from core.utils import get_coordinates_for_city
from pictures.models import StockPicture

from .constants import (
    APPLICATION_STATUS,
    DEPLOYED,
    NEW,
    ON_HOLD,
    REJECTED
)
from .managers import EventApplicationQuerySet
from .emails import (
    send_application_rejection_email,
    send_application_deployed_email
)


class EventApplication(models.Model):
    previous_event = models.ForeignKey(Event, null=True, blank=True,
                                       on_delete=models.deletion.SET_NULL)
    # workshop fields
    date = ApproximateDateField(validators=[validate_approximatedate])
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200, choices=countries)
    latlng = models.CharField(max_length=30, null=True, blank=True)
    website_slug = AutoSlugField(populate_from='city', editable=True)
    main_organizer_email = models.EmailField()
    main_organizer_first_name = models.CharField(max_length=30)
    main_organizer_last_name = models.CharField(max_length=30, blank=True,
                                                default="")
    created_at = models.DateTimeField(auto_now_add=True)

    # application fields
    about_you = models.TextField("About organizer")
    why = models.TextField("Motivations to organize")
    involvement = models.CharField("Involvement in Django Girls",
                                   max_length=100)
    experience = models.TextField("Experience with organizing other events")
    venue = models.TextField("Information about your potential venue", blank=True)
    sponsorship = models.TextField(
        "Information about your potential sponsorship")
    coaches = models.TextField("Information about your potential coaches")
    remote = models.BooleanField(default=False)
    tools = models.TextField("Information about how you will host your remote workshop",
                             blank=True)
    safety = models.TextField("Information about how you will ensure participants' and coaches' "
                              "safety during the Covid-19 pandemic",
                              blank=True)
    diversity = models.TextField("Information about how you intend to ensure your workshop is inclusive "
                                 "and promotes diversity")
    additional = models.TextField("Any additional information you think may help your application",
                                  blank=True)

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

    def save(self, *args, **kwargs):
        if not self.latlng:
            self.latlng = get_coordinates_for_city(self.city, self.get_country_display())
        super(EventApplication, self).save(*args, **kwargs)

    def create_event(self):
        """ Creates event based on the data from the EventApplication.
        """
        name = 'Django Girls {}'.format(self.city)
        email = '{}@djangogirls.org'.format(self.website_slug)

        event = Event.objects.create(
            date=self.date,
            city=self.city,
            country=self.get_country_display(),
            latlng=self.latlng,
            page_url=self.website_slug,
            name=name,
            page_title=name,
            email=email,
        )

        # populate content & menu from the default event
        event.add_default_content()
        event.add_default_menu()

        # Add a random cover picture to the event
        event.set_random_cover()
        event.save()

        return event

    def has_past_team_members(self, event):
        """ For repeated events, check whether there are any common
        team members who applied to organize again
        """
        previous_event = Event.objects.filter(
            city=self.city,
            country=self.get_country_display()
        ).exclude(pk=event.pk).order_by('-id').first()

        if previous_event:
            organizers = previous_event.team.all().values_list('email', flat=True)
            applicants = self.get_organizers_emails()
            return len(set(organizers).intersection(applicants)) > 0
        return False

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

        event = None
        previous_event = (
            Event.objects
            .filter(city=self.city, country=self.get_country_display())
            .order_by("-date")
            .first()
        )

        if previous_event:
            event = copy_event(previous_event, self.date)
        else:
            event = self.create_event()

        # add main organizer of the Event
        main_organizer = event.add_organizer(
            self.main_organizer_email,
            self.main_organizer_first_name,
            self.main_organizer_last_name,
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
        return event

    def send_deployed_email(self, event):
        # sort out Gmail accounts
        dummy_email, email_password = gmail_accounts.get_or_create_gmail(
            event_application=self,
            event=event
        )

        # TODO: remove organizers, who are no longer in org team if cloned
        send_application_deployed_email(
            event_application=self,
            event=event,
            email_password=email_password
        )

    def clean(self):
        if self.status == ON_HOLD and not self.comment:
            raise ValidationError({
                'comment': 'This field is required.'
            })

    def get_organizers_emails(self):
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
        related_name="coorganizers",
        on_delete=models.deletion.CASCADE)
    email = models.EmailField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True, default="")

    class Meta:
        verbose_name = "Co-organizer"
        verbose_name_plural = "Co-organizers"
