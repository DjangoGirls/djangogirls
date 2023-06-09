from datetime import date, timedelta

import icalendar
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.safestring import mark_safe
from django_date_extensions.fields import ApproximateDate, ApproximateDateField
from slack_sdk.errors import SlackApiError

from core.default_eventpage_content import get_default_eventpage_data, get_default_menu
from core.emails import notify_existing_user, notify_new_user
from core.models.managers.event import EventManager
from core.models.user import User
from core.validators import validate_approximatedate
from pictures.models import StockPicture


class Event(models.Model):
    name = models.CharField(max_length=200)
    date = ApproximateDateField(blank=True, validators=[validate_approximatedate])
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    latlng = models.CharField(verbose_name="latitude and longitude", max_length=30, null=True, blank=True)
    photo = models.ImageField(
        upload_to="event/cities/", null=True, blank=True, help_text="The best would be 356 x 210px"
    )
    photo_credit = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text=mark_safe(
            "Only use pictures with a " "<a href='https://creativecommons.org/licenses/'>Creative Commons license</a>."
        ),
    )
    photo_link = models.URLField(verbose_name="photo URL", null=True, blank=True)
    email = models.EmailField(verbose_name="event email", max_length=75, null=True, blank=True)
    main_organizer = models.ForeignKey(
        to=User, null=True, blank=True, related_name="main_organizer", on_delete=models.deletion.SET_NULL
    )
    team = models.ManyToManyField(to=User, blank=True)
    is_on_homepage = models.BooleanField(verbose_name="visible on homepage?", default=True)
    is_deleted = models.BooleanField(verbose_name="deleted?", default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    page_title = models.CharField(verbose_name="title", max_length=200, blank=True)
    page_description = models.TextField(
        verbose_name="description",
        blank=True,
        default="Django Girls is a one-day workshop about programming " "in Python and Django tailored for women.",
    )
    page_main_color = models.CharField(
        verbose_name="main color",
        max_length=6,
        blank=True,
        help_text="Main color of the chapter in HEX",
        default="FF9400",
    )
    page_custom_css = models.TextField(verbose_name="custom CSS rules", blank=True)
    page_url = models.CharField(
        verbose_name="URL slug",
        max_length=200,
        blank=True,
        help_text="Will be used as part of the event URL (djangogirls.org/______/)",
    )
    is_page_live = models.BooleanField(verbose_name="Website is ready", default=False)
    is_frozen = models.BooleanField(verbose_name="Event frozen", default=False)
    attendees_count = models.IntegerField(
        verbose_name="Number of attendees",
        null=True,
        blank=True,
    )
    applicants_count = models.IntegerField(
        verbose_name="Number of applicants",
        null=True,
        blank=True,
    )

    objects = EventManager()
    all_objects = models.Manager()  # This includes deleted objects

    # Flags for email states
    thank_you_email_sent = models.DateTimeField(null=True, blank=True)
    submit_information_email_sent = models.DateTimeField(null=True, blank=True)
    offer_help_email_sent = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}, {self.date}"

    class Meta:
        ordering = ("-date",)
        verbose_name_plural = "List of events"

    def is_upcoming(self):
        now = timezone.now()
        now = ApproximateDate(year=now.year, month=now.month, day=now.day)
        return self.date and now <= self.date

    @property
    def ical_uid(self):
        return f"event{self.pk}@djangogirls.org"

    @property
    def date_is_approximate(self):
        if not self.date:
            return True
        if not all((self.date.year, self.date.month, self.date.day)):
            return True
        return False

    @property
    def lnglat(self):
        """Returns X, Y coordinates.

        In most cases on the page we are operating on latitude, longitude string.
        This property returns the value in a swapped order of longitude, latitude
        also called X, Y instead. This is a standard required for GeoJSON coordinates
        required for the map JS library.
        """
        if not self.latlng:
            return ""

        try:
            lat, lng = self.latlng.split(", ")
        except ValueError:
            return ""

        return f"{lng}, {lat}"

    def as_ical(self):
        """
        Return a representation of the current event as an icalendar.Event.
        """
        if self.date_is_approximate:
            return None

        ymd = (self.date.year, self.date.month, self.date.day)
        event_date = date(*ymd)
        event = icalendar.Event()
        event.add("dtstart", event_date)
        event.add("dtend", event_date + timedelta(days=1))
        event.add("uid", self.ical_uid)
        event.add("summary", "Django Girls %s" % self.city)
        event.add("location", f"{self.country}, {self.city}")
        return event

    def organizers(self):
        members = [f"{x.get_full_name()} <{x.email}>" for x in self.team.all()]
        return ", ".join(members)

    def has_organizer(self, user):
        """
        Return whether a specific user is an organizer of the event
        """
        return self.main_organizer == user or self.team.filter(id=user.id).exists()

    @property
    def has_stats(self):
        return bool(self.applicants_count and self.attendees_count)

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def add_default_content(self):
        """Populate EventPageContent with default layout"""
        data = get_default_eventpage_data()

        for i, section in enumerate(data):
            section["position"] = i
            section["content"] = render_to_string(section["template"])
            del section["template"]
            self.content.create(**section)

    def add_default_menu(self):
        """Populate EventPageMenu with default links"""
        data = get_default_menu()

        for i, link in enumerate(data):
            link["position"] = i
            self.menu.create(**link)

    def invite_organizer_to_team(self, user, is_new_user, password):
        self.team.add(user)
        if is_new_user:
            errors = []
            try:
                user.invite_to_slack()
            except (ConnectionError, SlackApiError) as e:
                errors.append(f"Slack invite unsuccessful, reason: {e}")
            notify_new_user(user, event=self, password=password, errors=errors)
        else:
            notify_existing_user(user, event=self)

    def add_organizer(self, email, first_name, last_name):
        """
        Add organizer to the event.

        TODO: we need to think if create_organizers and create_events
        are the best place for this logic. Maybe we should move it back to
        the models.
        """
        defaults = {"first_name": first_name, "last_name": last_name, "is_staff": True, "is_active": True}
        user, created = User.objects.get_or_create(email=email, defaults=defaults)
        password = None
        if created:
            password = user.generate_password()
            user.add_to_organizers_group()

        self.invite_organizer_to_team(user, created, password)
        return user

    def set_random_cover(self):
        try:
            event_picture = StockPicture.objects.random_cover()
            self.photo = event_picture.photo
            self.photo_credit = event_picture.photo_credit
            self.photo_link = event_picture.photo_link
        except IndexError:
            # No StockPicture available
            pass

    def clone(self):
        """
        Clone this Event, for events with multiple website - that is English and non-English version.

        :return: the cloned Event
        :rtype: Event or NoneType
        """
        if not self.id:
            # this Event isn't saved yet...
            return None

        # first, get a copy of self (that isn't self), we'll save this into
        # the database as a new record by wiping the ID and re-saving
        clone = Event.objects.get(id=self.id)
        clone.id = None
        clone.name += " clone"
        clone.page_url += "_clone"
        clone.save()
        return clone

    def freeze(self):
        self.is_frozen = True
        self.is_on_homepage = False
        self.save(update_fields=["is_frozen", "is_on_homepage"])

    def unfreeze(self):
        self.is_frozen = False
        self.is_on_homepage = True
        self.save(update_fields=["is_frozen", "is_on_homepage"])


class EventPageContent(models.Model):
    event = models.ForeignKey(
        to=Event, null=False, blank=False, related_name="content", on_delete=models.deletion.CASCADE
    )
    name = models.CharField(max_length=100)
    content = models.TextField(help_text="HTML allowed")
    background = models.ImageField(
        upload_to="event/backgrounds/", null=True, blank=True, help_text="Optional background photo"
    )
    position = models.PositiveIntegerField(help_text="Position of the block on the website")
    is_public = models.BooleanField(default=False)
    coaches = models.ManyToManyField(to="coach.Coach", verbose_name="Coaches")
    sponsors = models.ManyToManyField(to="sponsor.Sponsor", verbose_name="Sponsors")

    def __str__(self):
        return f"{self.name} at {self.event}"

    class Meta:
        ordering = ("position",)
        verbose_name = "Website Content"


class EventPageMenu(models.Model):
    event = models.ForeignKey(to=Event, null=False, blank=False, related_name="menu", on_delete=models.deletion.CASCADE)
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255, help_text="http://djangogirls.org/city/<the value you enter here>")
    position = models.PositiveIntegerField(help_text="Order of menu")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("position",)
        verbose_name = "Website Menu"
