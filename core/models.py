from __future__ import unicode_literals

from datetime import date, datetime, timedelta
from slacker import Error as SlackerError

import icalendar
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import Group
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django_date_extensions.fields import ApproximateDate, ApproximateDateField

from .slack_client import user_invite
from .validators import validate_approximatedate
from .default_eventpage_content import (
    get_default_eventpage_data,
    get_default_menu,
)
from .emails import notify_existing_user, notify_new_user


class UserManager(auth_models.BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_superuser = user.is_staff = True
        user.save(using=self._db)
        return user


@python_2_unicode_compatible
class User(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Organizer"
        verbose_name_plural = "Organizers"

    def invite_to_slack(self):
        user_invite(self.email, self.first_name)

    def generate_password(self):
        password = User.objects.make_random_password()
        self.set_password(password)
        self.save()
        return password

    def add_to_organizers_group(self):
        try:
            group = Group.objects.get(name="Organizers")
        except Group.DoesNotExist:
            return

        self.groups.add(group)

    def __str__(self):
        if self.first_name == '' and self.last_name == '':
            return '{0}'.format(self.email)
        return '{0} ({1})'.format(self.get_full_name(), self.email)

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)


class EventManager(models.Manager):

    def get_queryset(self):
        return (super(EventManager, self).get_queryset()
                                         .filter(is_deleted=False))

    def public(self):
        """
        Only include events that are on the homepage.
        """
        return self.get_queryset().filter(is_on_homepage=True)

    def future(self):
        return self.public().filter(
            date__gte=datetime.now().strftime("%Y-%m-%d")
        ).order_by("date")

    def past(self):
        return self.public().filter(
            date__isnull=False,
            date__lt=datetime.now().strftime("%Y-%m-%d")
        ).order_by("-date")

# Event date can't be a year only


@python_2_unicode_compatible
class Event(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    date = ApproximateDateField(
        null=True, blank=False, validators=[validate_approximatedate])
    city = models.CharField(max_length=200, null=False, blank=False)
    country = models.CharField(max_length=200, null=False, blank=False)
    latlng = models.CharField("latitude and longitude", max_length=30, null=True, blank=True)
    photo = models.ImageField(upload_to="event/cities/", null=True, blank=True,
                              help_text="The best would be 356 x 210px")
    photo_credit = models.CharField(
        max_length=200, null=True, blank=True,
        help_text=mark_safe(
            "Only use pictures with a "
            "<a href='https://creativecommons.org/licenses/'>Creative Commons license</a>."))
    photo_link = models.URLField("photo URL", null=True, blank=True)
    email = models.EmailField(
        "event email", max_length=75, null=True, blank=True)
    main_organizer = models.ForeignKey(
        User, null=True, blank=True, related_name="main_organizer")
    team = models.ManyToManyField(User, blank=True)
    is_on_homepage = models.BooleanField("visible on homepage?", default=True)
    is_deleted = models.BooleanField("deleted?", default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    page_title = models.CharField("title", max_length=200, blank=True)
    page_description = models.TextField(
        "description", blank=True,
        default="Django Girls is a one-day workshop about programming "
                "in Python and Django tailored for women.")
    page_main_color = models.CharField(
        "main color", max_length=6, blank=True,
        help_text="Main color of the chapter in HEX", default="FF9400")
    page_custom_css = models.TextField("custom CSS rules", blank=True)
    page_url = models.CharField(
        "URL slug", max_length=200, blank=True,
        help_text="Will be used as part of the event URL (djangogirls.org/______/)")
    is_page_live = models.BooleanField("Website is ready", default=False)

    attendees_count = models.IntegerField(
        null=True, blank=True, verbose_name="Number of attendees")
    applicants_count = models.IntegerField(
        null=True, blank=True, verbose_name="Number of applicants")

    objects = EventManager()
    all_objects = models.Manager()  # This includes deleted objects

    # Flags for email states
    thank_you_email_sent = models.DateTimeField(null=True, blank=True)
    submit_information_email_sent = models.DateTimeField(null=True, blank=True)
    offer_help_email_sent = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '{}, {}'.format(self.name, self.date)

    class Meta:
        ordering = ('-date', )
        verbose_name_plural = "List of events"

    def is_upcoming(self):
        if not self.date:
            return False
        now = timezone.now()
        now = ApproximateDate(year=now.year, month=now.month, day=now.day)
        if now < self.date:
            return True
        return False

    @property
    def ical_uid(self):
        return "event%d@djangogirls.org" % self.pk

    @property
    def date_is_approximate(self):
        if not self.date:
            return True
        if not all((self.date.year, self.date.month, self.date.day)):
            return True
        return False

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
        event.add("location", "%s, %s" % (self.country, self.city))
        return event

    def organizers(self):
        members = ["{} <{}>".format(x.get_full_name(), x.email)
                   for x in self.team.all()]
        return ", ".join(members)

    @property
    def has_stats(self):
        return bool(self.applicants_count and self.attendees_count)

    def delete(self):
        self.is_deleted = True
        self.save()

    def add_default_content(self):
        """Populate EventPageContent with default layout"""
        data = get_default_eventpage_data()

        for i, section in enumerate(data):
            section['position'] = i
            section['content'] = render_to_string(section['template'])
            del section['template']
            self.content.create(**section)

    def add_default_menu(self):
        """Populate EventPageMenu with default links"""
        data = get_default_menu()

        for i, link in enumerate(data):
            link['position'] = i
            self.menu.create(**link)

    def invite_organizer_to_team(self, user, is_new_user, password):
        self.team.add(user)
        if is_new_user:
            errors = []
            try:
                user.invite_to_slack()
            except (ConnectionError, SlackerError) as e:
                errors.append(
                    'Slack invite unsuccessful, reason: {}'.format(e)
                )
            notify_new_user(user, event=self, password=password, errors=errors)
        else:
            notify_existing_user(user, event=self)

    def add_organizer(self, email, first_name, last_name):
        """
            Add organizer to the event.

            TODO: we need to think if create_organizers and create_events
            are the best place for these logic. Maybe we should move it back to
            the models.
        """
        defaults = {
            "first_name": first_name,
            "last_name": last_name,
            "is_staff": True,
            "is_active": True
        }
        user, created = User.objects.get_or_create(
            email=email,
            defaults=defaults
        )
        password = None
        if created:
            password = user.generate_password()
            user.add_to_organizers_group()

        self.invite_organizer_to_team(user, created, password)
        return user


@python_2_unicode_compatible
class EventPageContent(models.Model):
    event = models.ForeignKey(Event, null=False,
                              blank=False, related_name="content")
    name = models.CharField(null=False, blank=False, max_length=100)
    content = models.TextField(
        null=False, blank=False, help_text="HTML allowed")
    background = models.ImageField(
        upload_to="event/backgrounds/", null=True, blank=True,
        help_text="Optional background photo")
    position = models.PositiveIntegerField(
        null=False, blank=False,
        help_text="Position of the block on the website")
    is_public = models.BooleanField(null=False, blank=False, default=False)
    coaches = models.ManyToManyField("coach.Coach", verbose_name='Coaches')
    sponsors = models.ManyToManyField("sponsor.Sponsor", verbose_name='Sponsors')

    def __str__(self):
        return "%s at %s" % (self.name, self.event)

    class Meta:
        ordering = ("position", )
        verbose_name = "Website Content"


@python_2_unicode_compatible
class EventPageMenu(models.Model):
    event = models.ForeignKey(Event, null=False,
                              blank=False, related_name="menu")
    title = models.CharField(max_length=255, null=False, blank=False)
    url = models.CharField(
        max_length=255, null=False, blank=False,
        help_text="http://djangogirls.org/city/<the value you enter here>")
    position = models.PositiveIntegerField(
        null=False, blank=False, help_text="Order of menu")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("position", )
        verbose_name = "Website Menu"
