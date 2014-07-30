from django.db import models
from django.contrib.auth import models as auth_models

from django.contrib.auth.models import User

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


class Event(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    date = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=200, null=False, blank=False)
    country = models.CharField(max_length=200, null=False, blank=False)

    main_organizer = models.ForeignKey(User, null=True, blank=True, related_name="main_organizer")
    team = models.ManyToManyField(User, null=True, blank=True)

    def __unicode__(self):
        return self.name

class EventPage(models.Model):
    event = models.OneToOneField(Event, primary_key=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True, default='Django Girls is a one-day workshop about programming in Python and Django tailored for women.')
    main_color = models.CharField(max_length=6, null=True, blank=True, help_text='Main color of the chapter in HEX', default='FF9400')
    custom_css = models.TextField(null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)

    is_live = models.BooleanField(null=False, blank=False, default=False)

    def __unicode__(self):
        return 'Website for {0}'.format(self.event)

class EventPageContent(models.Model):
    page = models.ForeignKey(EventPage, null=False, blank=False)
    name = models.CharField(null=False, blank=False, max_length=100)
    content = models.TextField(null=False, blank=False, help_text="HTLM allowed")
    background = models.ImageField(upload_to="event/backgrounds/", null=True, blank=True, help_text="Optional background photo")
    position = models.IntegerField(null=False, blank=False, help_text="Position of the block on the website")

    is_public = models.BooleanField(null=False, blank=False, default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('position', )

class EventPageMenu(models.Model):
    page = models.ForeignKey(EventPage, null=False, blank=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    url = models.CharField(max_length=255, null=False, blank=False)
    position = models.IntegerField(null=False, blank=False, help_text="Order of menu")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('position', )
