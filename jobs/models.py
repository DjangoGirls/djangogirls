from __future__ import unicode_literals
from datetime import timedelta

from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone

from django.db import models
from django_countries.fields import CountryField

from django.template.loader import get_template
from django.template import Context

from core.models import User

from jobs.community_mails import send_job_mail, send_meetup_mail


class PublishFlowManager(models.Manager):

    def get_queryset(self):
        now = timezone.now().date().strftime("%Y-%m-%d")
        return super(PublishFlowManager, self).get_queryset().extra(
            select={'not_expired': "coalesce(expiration_date > '%s', 1)" % now})


class VisiblePublishFlowManager(PublishFlowManager):

    def get_queryset(self):
        return super(VisiblePublishFlowManager, self).get_queryset().filter(
            review_status=PublishFlowModel.PUBLISHED,
            expiration_date__gte=timezone.now()
        )


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
    STATUSES = (
        (OPEN, 'Open'),
        (UNDER_REVIEW, 'Under review'),
        (READY_TO_PUBLISH, 'Ready to publish'),
        (REJECTED, 'Rejected'),
        (PUBLISHED, 'Published'),
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

    objects = PublishFlowManager()
    visible_objects = VisiblePublishFlowManager()

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
        subject = '{0} was rejected.'.format(self.title)
        model_name = self._meta.model_name
        context = Context({
                    'status': self.get_review_status_display(),
                    'option': model_name,
                    'reviewers_comment': self.reviewers_comment,
                })
        message_plain = get_template(
            'jobs/email_templates/status.txt').render(context)
        message_html = get_template(
            'jobs/email_templates/status.html').render(context)
        recipient = self.contact_email
        if model_name == 'job':
            send_job_mail(
                    subject,
                    message_plain,
                    message_html,
                    recipient
                )
        elif model_name == 'meetup':
            send_meetup_mail(
                subject,
                message_plain,
                message_html,
                recipient,
            )

    def restore(self, user):
        assert self.review_status == self.REJECTED
        self.reviewer = user
        self.review_status = self.UNDER_REVIEW
        self.save()

    def publish(self):
        assert self.is_ready_to_publish()
        self.published_date = timezone.now()
        # the line below covers the situation when there is no expiration date
        # set or when somebody wants to republish an expired post but
        # hasn't changed the expiration date
        if not self.expiration_date or self.expiration_date < self.published_date.date():
            self.expiration_date = self.published_date + timedelta(60)
        self.review_status = self.PUBLISHED
        self.save()
        subject = '{0} is now published.'.format(self.title)
        model_name = self._meta.model_name
        context = Context({
                    'status': self.get_review_status_display(),
                    'option': model_name,
                    'reviewers_comment': self.reviewers_comment,
                })
        message_plain = get_template(
            'jobs/email_templates/status.txt').render(context)
        message_html = get_template(
            'jobs/email_templates/status.html').render(context)
        recipient = self.contact_email
        if model_name == 'job':
            send_job_mail(
                    subject,
                    message_plain,
                    message_html,
                    recipient
                )
        elif model_name == 'meetup':
            send_meetup_mail(
                subject,
                message_plain,
                message_html,
                recipient,
            )


@python_2_unicode_compatible
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

    def __str__(self):
        return "{0}, {1}".format(self.title, self.company)


@python_2_unicode_compatible
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

    def __str__(self):
        return "{0}, {1}".format(self.title, self.city)
