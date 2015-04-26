from datetime import timedelta

from django.utils import timezone

from django.db import models
from django_countries.fields import CountryField
from django.conf import settings

from core.models import User


class PublishFlowModel(models.Model):
    """
    An abstract class model that handles all logic related to publishing
    an item that needs to be reviewed
    """
    OPEN = 'OPN'
    UNDER_REVIEW = 'URE'
    READY_TO_PUBLISH = 'RTP'
    REJECTED = 'REJ'
    PUBLISHED = 'PUB'
    EXPIRED = 'EXP'
    STATUSES = (
        (OPEN, 'Open'),
        (UNDER_REVIEW, 'Under review'),
        (READY_TO_PUBLISH, 'Ready to publish'),
        (REJECTED, 'Rejected'),
        (PUBLISHED, 'Published'),
        (EXPIRED, 'Expired'),
    )

    reviewer = models.ForeignKey(
        User,
        related_name="%(app_label)s_%(class)s_related",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    review_status = models.CharField(max_length=3, choices=STATUSES, default=OPEN)
    reviewers_comment = models.TextField(blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateField(
        blank=True,
        null=True,
        help_text="Automatically is set 60 days from posting. You can"
                  " override this."
    )

    class Meta:
        abstract = True
        ordering = ['-published_date']

    def is_ready_to_publish(self):
        return self.review_status == self.READY_TO_PUBLISH

    def assign(self, user):
        assert self.review_status == self.OPEN
        self.reviewer = user
        self.review_status = self.UNDER_REVIEW
        self.save()

    def unassign(self):
        assert self.review_status == self.UNDER_REVIEW
        self.reviewer = None
        self.review_status = self.OPEN
        self.save()

    def accept(self):
        assert self.review_status == self.UNDER_REVIEW
        self.review_status = self.READY_TO_PUBLISH
        self.save()

    def reject(self):
        assert self.review_status in [self.UNDER_REVIEW, self.READY_TO_PUBLISH, self.PUBLISHED]
        self.review_status = self.REJECTED
        self.published_date = None
        self.save()

    def restore(self):
        assert self.review_status == self.REJECTED
        self.review_status = self.UNDER_REVIEW
        self.save()

    def publish(self):
        assert self.is_ready_to_publish()
        self.published_date = timezone.now()
        if not self.expiration_date:
            self.expiration_date = self.published_date + timedelta(60)
        self.review_status = self.PUBLISHED
        self.save()


class Job(PublishFlowModel):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    website = models.URLField(
        help_text="Link to your offer or company website.",
        blank=True,
        null=True
    )
    contact_email = models.EmailField(max_length=255)
    cities = models.CharField(max_length=255)
    country = CountryField()
    description = models.TextField()
    remote_work = models.BooleanField(
        default=False,
    )
    relocation = models.BooleanField(
        default=False,
    )

    class Meta(PublishFlowModel.Meta):
        unique_together = (("company", "title"),)

    def __unicode__(self):
        return "{0}, {1}".format(self.title, self.company)


class Meetup(PublishFlowModel):

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
    meetup_start_date = models.DateTimeField(
        null=True,
        help_text="If this is a recurring meetup/event, please enter a start date.\
            Date format: YYYY-MM-DD"
    )
    meetup_end_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date format: YYYY-MM-DD"
    )

    class Meta(PublishFlowModel.Meta):
        unique_together = (("title", "city"),)

    def __unicode__(self):
        return u"{0}, {1}".format(self.title, self.city)
