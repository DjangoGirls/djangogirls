from datetime import timedelta

from django.utils import timezone

from django.db import models
from django_countries.fields import CountryField
from django.conf import settings

from core.models import User


class Company(models.Model):

    name = models.CharField(max_length=500, unique=True)
    website = models.URLField()


    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Job(models.Model):

    title = models.CharField(max_length=500)
    company = models.ForeignKey('Company', related_name="company")
    contact_email = models.EmailField(max_length=254)
    city = models.CharField(max_length=100)
    country = CountryField()
    description = models.TextField(max_length=5000)
    reviewer = models.ForeignKey(
        User, 
        related_name="jobs",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    review_status = models.BooleanField(default=False, help_text="Check if reviewed")
    reviewers_comment = models.TextField(max_length=5000, blank=True, null=True)
    ready_to_publish = models.BooleanField(default=False)
    published_date = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Automatically is set 60 days from posting. You can override this."
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
            if self.expiration_date:
                self.expiration_date = self.published_date + timedelta(60)
                self.save()


    def __unicode__(self):
        return "{0}, {1}".format(self.title, self.company)

