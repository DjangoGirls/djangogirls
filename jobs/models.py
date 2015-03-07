from datetime import timedelta

from django.utils import timezone

from django.db import models
from django_countries.fields import CountryField
from django.conf import settings

from core.models import User


class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    website = models.URLField(
        help_text="Link to your offer or company website.",
        blank=True,
        null=True
    )
    contact_email = models.EmailField(max_length=255)
    city = models.CharField(max_length=255)
    country = CountryField()
    description = models.TextField()
    reviewer = models.ForeignKey(
        User,
        related_name="jobs",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    review_status = models.BooleanField(default=False,
                                        help_text="Check if reviewed")
    reviewers_comment = models.TextField(blank=True, null=True)
    ready_to_publish = models.BooleanField(default=False)
    published_date = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateField(
        blank=True,
        null=True,
        help_text="Automatically is set 60 days from posting. You can"
                  " override this."
    )

    class Meta:
        unique_together = (("company", "title"),)
        ordering = ['-published_date']

    def publish(self):
        if self.ready_to_publish:
            self.published_date = timezone.now()
            self.save()

    def set_expiration_date(self):
        if self.published_date:
            if self.ready_to_publish and not self.expiration_date:
                self.expiration_date = self.published_date + timedelta(60)
                self.save()
            if self.ready_to_publish and self.expiration_date:
                self.expiration_date = self.published_date + timedelta(60)
                self.save()

    def __unicode__(self):
        return "{0}, {1}".format(self.title, self.company)


class Meetup(models.Model):

    MEETUP = 'MEET'
    CONFERENCE = 'CONF'
    WORKSHOP = 'WORK'
    MEETUP_TYPES = (
        (MEETUP, 'meetup'),
        (CONFERENCE, 'conference'),
        (WORKSHOP, 'workshop'),
    )

    title = models.CharField(max_length=255)
    organisation = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    meetup_type = models.CharField(
        max_length=4,
        choices=MEETUP_TYPES,
        default=MEETUP
    )
    contact_email = models.EmailField(max_length=255)
    website = models.URLField(
        help_text="Link to your meetup or organisation website.",
        blank=True,
        null=True
    )
    city = models.CharField(max_length=255)
    country = CountryField()
    description = models.TextField()
    is_recurring = models.BooleanField(
        default=False,
    )
    #TODO this field should be required if the is_recurring is True
    recurrence = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Provide details of recurrence if applicable."
    )
    meetup_date = models.DateTimeField(
        null=True,
        help_text="If this is a recurring meetup/event, please enter a start date.\
            Date format: MM/DD/YYYY"
    )
    reviewer = models.ForeignKey(
        User,
        related_name="meetups",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    review_status = models.BooleanField(
        default=False,
        help_text="Check if reviewed",
    )
    reviewers_comment = models.TextField(blank=True, null=True,)
    ready_to_publish = models.BooleanField(default=False)
    published_date = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateField(
        blank=True,
        null=True,
        help_text="Automatically is set 60 days from posting. You can "
                  "override this.",
    )

    class Meta:
        unique_together = (("title", "city"),)
        ordering = ['-published_date']

    def publish(self):
        assert self.ready_to_publish
        self.published_date = timezone.now()
        if not self.expiration_date:
            self.expiration_date = self.published_date + timedelta(60)
        self.save()

    def __unicode__(self):
        return u"{0}, {1}".format(self.title, self.city)
