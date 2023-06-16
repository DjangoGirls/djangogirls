from django.db import models
from django.utils import timezone

from .emails import (
    send_promotional_material_email,
    send_prospective_sponsor_email,
    send_renewal_email,
    send_thank_you_email,
)

PATREON_LEVELS = [
    (100, "$100/month"),
    (250, "$250/month"),
    (500, "$500/month"),
    (1000, "$1,000/month"),
]

ANNUAL_SPONSOR_LEVELS = [
    (500, "Bronze ($500)"),
    (1000, "Silver ($1000)"),
    (2500, "Gold ($2,500)"),
    (5000, "Platinum ($5,000)"),
    (10000, "Diamond ($10,000)"),
]


class GlobalPartner(models.Model):
    company_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    contact_email = models.EmailField(max_length=100)
    prospective_sponsor = models.BooleanField(default=False)
    patreon_sponsor = models.BooleanField(default=False)
    patreon_level_per_month = models.IntegerField(blank=True, null=True, choices=PATREON_LEVELS)
    sponsor_level_annual = models.IntegerField(blank=True, null=True, choices=ANNUAL_SPONSOR_LEVELS)
    date_joined = models.DateField(blank=True, null=True)
    contacted = models.BooleanField(default=False)
    date_contacted = models.DateField(blank=True, null=True)
    next_renewal_date = models.DateField(blank=True, null=True)
    logo = models.ImageField(upload_to="uploads", blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    is_displayed = models.BooleanField(default=False)
    website_url = models.URLField(blank=True, null=True)
    style = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.company_name

    def update_details(self):
        self.contacted = True
        self.date_contacted = timezone.now()
        self.save()

    def send_prospective_sponsor_email(self):
        send_prospective_sponsor_email(self.contact_person, self.contact_email)
        self.update_details()

    def send_renewal_email(self):
        send_renewal_email(self.contact_person, self.contact_email)
        self.update_details()

    def send_promotional_material_email(self):
        send_promotional_material_email(
            self.contact_person, self.contact_email, self.prospective_sponsor, self.sponsor_level_annual
        )
        self.update_details()

    def send_thank_you_email(self):
        send_thank_you_email(self.contact_person, self.contact_email)
        self.update_details()
