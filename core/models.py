from datetime import date, datetime, timedelta

import icalendar

from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import User

from django_date_extensions.fields import ApproximateDateField

class UserManager(auth_models.BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_superuser = user.is_staff = True
        user.save(using=self._db)
        return user


class User(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Organizer'
        verbose_name_plural = 'Organizers'

    def __unicode__(self):
        return u'{0} ({1})'.format(self.get_full_name(), self.email)

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return u'{0} {1}'.format(self.first_name, self.last_name)


class EventQuerySet(models.QuerySet):
    def public(self):
        """
        Only include events that are on the homepage.
        """
        return self.filter(is_on_homepage=True)

    def future(self):
        return self.public().filter(date__gte=datetime.now().strftime('%Y-%m-%d')).order_by('date')

    def past(self):
        return self.public().filter(date__lt=datetime.now().strftime('%Y-%m-%d')).order_by('-date')


class Event(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    date = ApproximateDateField(null=True, blank=True)
    city = models.CharField(max_length=200, null=False, blank=False)
    country = models.CharField(max_length=200, null=False, blank=False)
    latlng = models.CharField(max_length=30, null=True, blank=True)
    photo = models.ImageField(upload_to="event/cities/", null=True, blank=True, help_text="The best would be 356 x 210px")
    photo_credit = models.CharField(max_length=200, null=True, blank=True)
    photo_link = models.URLField(null=True, blank=True)
    main_organizer = models.ForeignKey(User, null=True, blank=True, related_name="main_organizer")
    team = models.ManyToManyField(User, null=True, blank=True)
    is_on_homepage = models.BooleanField(default=False)

    objects = EventQuerySet.as_manager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "List of events"

    @property
    def ical_uid(self):
        return 'event%d@djangogirls.org' % self.pk

    def as_ical(self):
        """
        Return a representation of the current event as an icalendar.Event.
        """
        ymd = (self.date.year, self.date.month, self.date.day)
        if not all(ymd):
            return None
        event_date = date(*ymd)
        event = icalendar.Event()
        event.add('dtstart', event_date)
        event.add('dtend', event_date + timedelta(days=1))
        event.add('uid', self.ical_uid)
        event.add('summary', u'Django Girls %s' % self.city)
        event.add('location', u'%s, %s' % (self.country, self.city))
        return event

class EventPage(models.Model):
    event = models.OneToOneField(Event, primary_key=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True, default='Django Girls is a one-day workshop about programming in Python and Django tailored for women.')
    main_color = models.CharField(max_length=6, null=True, blank=True, help_text='Main color of the chapter in HEX', default='FF9400')
    custom_css = models.TextField(null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)

    is_live = models.BooleanField(null=False, blank=False, default=False)

    def __unicode__(self):
        return 'Website for %s' % self.event.name

    class Meta:
        verbose_name = "Website"

class EventPageContent(models.Model):
    page = models.ForeignKey(EventPage, null=False, blank=False)
    name = models.CharField(null=False, blank=False, max_length=100)
    content = models.TextField(null=False, blank=False, help_text="HTML allowed")
    background = models.ImageField(upload_to="event/backgrounds/", null=True, blank=True, help_text="Optional background photo")
    position = models.PositiveIntegerField(null=False, blank=False, help_text="Position of the block on the website")

    is_public = models.BooleanField(null=False, blank=False, default=False)

    def __unicode__(self):
        return "%s at %s" % (self.name, self.page.event)

    class Meta:
        ordering = ('position', )
        verbose_name = "Website Content"


class EventPageMenu(models.Model):
    page = models.ForeignKey(EventPage, null=False, blank=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    url = models.CharField(max_length=255, null=False, blank=False)
    position = models.PositiveIntegerField(null=False, blank=False, help_text="Order of menu")

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('position', )
        verbose_name = "Website Menu"

class Sponsor(models.Model):
    event_page_content = models.ForeignKey(EventPageContent, null=False, blank=False)
    name = models.CharField(max_length=200, null=True, blank=True)
    logo = models.ImageField(upload_to="event/sponsors/", null=True, blank=True, help_text="Make sure logo is not bigger than 200 pixels wide")
    url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    position = models.PositiveIntegerField(null=False, blank=False, help_text="Position of the sponsor")

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('position', )

class Coach(models.Model):
    event_page_content = models.ForeignKey(EventPageContent, null=False, blank=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    twitter_handle = models.CharField(max_length=200, null=True, blank=True, help_text="No @, No http://, just username")
    photo = models.ImageField(upload_to="event/coaches/", null=True, blank=True, help_text="For best display keep it square")
    url = models.URLField(null=True, blank=True)


    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('?',)
        verbose_name_plural = "Coaches"

class Postmortem(models.Model):
    event = models.ForeignKey(Event, null=False, blank=False)
    attendees_count = models.IntegerField(null=False, blank=False, verbose_name="Number of attendees")
    applicants_count = models.IntegerField(null=False, blank=False, verbose_name="Number of applicants")

    discovery = models.TextField(null=True, blank=True, verbose_name="What was the most important thing you discovered during the workshop?")
    feedback = models.TextField(null=True, blank=True, verbose_name="How we can make DjangoGirls better?")
    costs = models.TextField(null=True, blank=True, verbose_name="What are the total costs of the event?", help_text="We only collect this information for statistics and advice for future organizers.")
    comments = models.TextField(null=True, blank=True, verbose_name="Anything else you want to share with us?")

    def __unicode__(self):
        return self.event.city

class Story(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    post_url = models.URLField(null=False, blank=False)
    image = models.ImageField(upload_to="stories/", null=False, blank=False)
    created = models.DateField(auto_now_add=True, null=False, blank=False)

    def __unicode__(self):
        return self.name
