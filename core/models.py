from __future__ import unicode_literals

from datetime import date, datetime, timedelta
from smtplib import SMTPException

import icalendar
from django.contrib.auth import models as auth_models
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.safestring import mark_safe
from django_date_extensions.fields import ApproximateDate, ApproximateDateField
from easy_thumbnails.exceptions import InvalidImageFormatError
from easy_thumbnails.files import get_thumbnailer

DEFAULT_COACH_PHOTO = static('img/global/coach-empty.jpg')


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


def validate_approximatedate(date):
    if date.month == 0:
        raise ValidationError(
            'Event date can\'t be a year only. Please, provide at least a month and a year.')


@python_2_unicode_compatible
class Event(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    date = ApproximateDateField(null=True, blank=False, validators=[
                                validate_approximatedate])
    city = models.CharField(max_length=200, null=False, blank=False)
    country = models.CharField(max_length=200, null=False, blank=False)
    latlng = models.CharField(max_length=30, null=True, blank=True)
    photo = models.ImageField(upload_to="event/cities/", null=True, blank=True,
                              help_text="The best would be 356 x 210px")
    photo_credit = models.CharField(max_length=200, null=True, blank=True, help_text=mark_safe("Only use pictures with a <a href='https://creativecommons.org/licenses/'>creative commons license</a>."))
    photo_link = models.URLField(null=True, blank=True)
    email = models.EmailField(max_length=75, null=True, blank=True)
    main_organizer = models.ForeignKey(
        User, null=True, blank=True, related_name="main_organizer")
    team = models.ManyToManyField(User, blank=True)
    is_on_homepage = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    objects = EventManager()
    all_objects = models.Manager()  # This includes deleted objects

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('pk', )
        verbose_name_plural = "List of events"

    def is_upcoming(self):
        now = timezone.now()
        now = ApproximateDate(year=now.year, month=now.month, day=now.day)
        if now < self.date:
            return True
        return False

    @property
    def ical_uid(self):
        return "event%d@djangogirls.org" % self.pk

    def as_ical(self):
        """
        Return a representation of the current event as an icalendar.Event.
        """
        if not self.date:
            return None
        ymd = (self.date.year, self.date.month, self.date.day)
        if not all(ymd):
            return None
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

    def delete(self):
        self.is_deleted = True
        self.save()


class EventPageManager(models.Manager):

    def get_queryset(self):
        return super(EventPageManager, self).get_queryset().filter(is_deleted=False)


@python_2_unicode_compatible
class EventPage(models.Model):
    event = models.OneToOneField(Event, primary_key=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(
        null=True, blank=True,
        default="Django Girls is a one-day workshop about programming "
                "in Python and Django tailored for women.")
    main_color = models.CharField(
        max_length=6, null=True, blank=True,
        help_text="Main color of the chapter in HEX", default="FF9400")
    custom_css = models.TextField(null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)

    is_live = models.BooleanField(null=False, blank=False, default=False)
    is_deleted = models.BooleanField(default=False)

    objects = EventPageManager()
    all_objects = models.Manager()  # This includes deleted objects

    def __str__(self):
        return "Website for %s" % self.event.name

    class Meta:
        ordering = ('title', )
        verbose_name = "Website"

    def delete(self):
        self.is_deleted = True
        self.save()


@python_2_unicode_compatible
class ContactEmail(models.Model):
    CHAPTER, SUPPORT = 'chapter', 'support'
    CONTACT_TYPE_CHOICES = (
        (CHAPTER, 'Django Girls Local Organizers'),
        (SUPPORT, 'Django Girls HQ (Support Team)'),
    )

    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
    sent_to = models.EmailField(max_length=128)
    message = models.TextField()
    event = models.ForeignKey(
        'core.Event', help_text='required for contacting a chapter',
        null=True, blank=True
    )
    contact_type = models.CharField(
        verbose_name="Who do you want to contact?",
        max_length=20, choices=CONTACT_TYPE_CHOICES, blank=False,
        default=CHAPTER
    )
    created_at = models.DateTimeField(auto_now_add=True)
    sent_successfully = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return "%s to %s" % (self.email, self.sent_to)

    def save(self, *args, **kwargs):
        self.sent_to = self._get_to_email()
        email = EmailMessage(
            self._get_subject(),
            self.message,
            "Django Girls Contact <hello@djangogirls.org>",
            [self.sent_to],
            reply_to=["{} <{}>".format(self.name, self.email)],
            headers={'Reply-To': "{} <{}>".format(self.name, self.email)}
            # Seems like this is needed for Mandrill
        )
        try:
            email.send(fail_silently=False)
        except SMTPException:
            self.sent_successfully = False

        super(ContactEmail, self).save(*args, **kwargs)

    def _get_to_email(self):
        if self.event and self.event.email:
            return self.event.email
        return 'hello@djangogirls.org'

    def _get_subject(self):
        return "%s - from the djangogirls.org website" % self.name


@python_2_unicode_compatible
class EventPageContent(models.Model):
    page = models.ForeignKey(EventPage, null=False,
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
    coaches = models.ManyToManyField("core.Coach", verbose_name='Coaches')
    sponsors = models.ManyToManyField("core.Sponsor", verbose_name='Sponsors')

    def __str__(self):
        return "%s at %s" % (self.name, self.page.event)

    class Meta:
        ordering = ("position", )
        verbose_name = "Website Content"


@python_2_unicode_compatible
class EventPageMenu(models.Model):
    page = models.ForeignKey(EventPage, null=False,
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


@python_2_unicode_compatible
class Sponsor(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    logo = models.ImageField(
        upload_to="event/sponsors/", null=True, blank=True,
        help_text="Make sure logo is not bigger than 200 pixels wide")
    url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name", )

    def logo_display_for_admin(self):
        if self.logo:
            return "<a href=\"{}\" target=\"_blank\"><img src=\"{}\" width=\"100\" /></a>".format(
                self.logo.url, self.logo.url)
        else:
            return "No logo"
    logo_display_for_admin.allow_tags = True


@python_2_unicode_compatible
class Coach(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    twitter_handle = models.CharField(
        max_length=200, null=True, blank=True,
        help_text="No @, No http://, just username")
    photo = models.ImageField(
        upload_to="event/coaches/", null=True, blank=True,
        help_text="For best display keep it square")
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Coaches"

    def photo_display_for_admin(self):
        coach_change_url = reverse("admin:core_coach_change", args=[self.id])
        return """
            <a href=\"{}\" target=\"_blank\">
                <img src=\"{}\" width=\"100\" />
            </a>""".format(coach_change_url, self.photo_url)
    photo_display_for_admin.allow_tags = True

    @property
    def photo_url(self):
        if self.photo:
            try:
                return get_thumbnailer(self.photo)['coach'].url
            except InvalidImageFormatError:
                return DEFAULT_COACH_PHOTO

        return DEFAULT_COACH_PHOTO


@python_2_unicode_compatible
class Postmortem(models.Model):
    event = models.ForeignKey(Event, null=False, blank=False)
    attendees_count = models.IntegerField(null=False, blank=False,
                                          verbose_name="Number of attendees")
    applicants_count = models.IntegerField(null=False, blank=False,
                                           verbose_name="Number of applicants")

    discovery = models.TextField(null=True, blank=True,
                                 verbose_name="What was the most important thing you discovered during the workshop?")
    feedback = models.TextField(null=True, blank=True,
                                verbose_name="How we can make DjangoGirls better?")
    costs = models.TextField(null=True, blank=True,
                             verbose_name="What are the total costs of the event?",
                             help_text="We only collect this information for statistics and advice for future organizers.")
    comments = models.TextField(null=True, blank=True,
                                verbose_name="Anything else you want to share with us?")

    class Meta:
        verbose_name = "Statistics"
        verbose_name_plural = "Statistics"

    def __str__(self):
        return self.event.city


@python_2_unicode_compatible
class Story(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    content = models.TextField(null=True)
    post_url = models.URLField(null=False, blank=False)
    image = models.ImageField(upload_to="stories/", null=True)
    created = models.DateField(auto_now_add=True, null=False, blank=False)
    # False means a regular blogpost, not a story
    is_story = models.BooleanField(default=True)

    def __str__(self):
        return self.name
