from django.db import models

from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    date = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=200, null=False, blank=False)
    country = models.CharField(max_length=200, null=False, blank=False)

    main_organizer = models.ForeignKey(User, null=True, blank=True, related_name="main_organizer")
    team = models.ManyToManyField(User, null=True, blank=True)

    def __str__(self):
        return self.name

class EventPage(models.Model):
    event = models.OneToOneField(Event, primary_key=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    main_color = models.CharField(max_length=6, null=True, blank=True, help_text='Main color of the chapter in HEX')
    custom_css = models.TextField(null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)

    is_live = models.BooleanField(null=False, blank=False, default=False)

    def __str__(self):
        return 'Website for {0}'.format(self.event)

class EventPageContent(models.Model):
    page = models.ForeignKey(EventPage, null=False, blank=False)
    name = models.CharField(null=False, blank=False, max_length=100)
    content = models.TextField(null=False, blank=False, help_text="HTLM allowed")
    background = models.ImageField(upload_to="event/backgrounds/", null=True, blank=True, help_text="Optional background photo")
    position = models.IntegerField(null=False, blank=False, help_text="Position of the block on the website")

    is_public = models.BooleanField(null=False, blank=False, default=False)

    def __str__(self):
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
