from django.db import models
from django.utils import timezone

from .emails import (
    send_promotional_material_email,
    send_prospective_sponsor_email,
    send_renewal_email,
    send_thank_you_email,
)

PATREON_LEVELS = [
    ("$100/month", "$100/month"),
    ("$250/month", "$250/month"),
    ("$500/month", "$500/month"),
    ("$1,000/month", "$1,000/month"),
]

ANNUAL_SPONSOR_LEVELS = [
    ("Bronze ($500)", "Bronze ($500)"),
    ("Silver ($1000)", "Silver ($1000)"),
    ("Gold ($2,500)", "Gold ($2,500)"),
    ("Platinum ($5,000)", "Platinum ($5,000)"),
    ("Diamond ($10,000", "Diamond ($10,000"),
]


class GlobalPartner(models.Model):
    company_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    contact_email = models.EmailField(max_length=100)
    prospective_sponsor = models.BooleanField(default=False)
    patreon_sponsor = models.BooleanField(default=False)
    patreon_sponsor_level = models.CharField(max_length=20, blank=True, null=True, choices=PATREON_LEVELS)
    sponsor_level = models.CharField(max_length=20, blank=True, null=True, choices=ANNUAL_SPONSOR_LEVELS)
    date_joined = models.DateField(blank=True, null=True)
    contacted = models.BooleanField(default=False)
    date_contacted = models.DateField(blank=True, null=True)
    next_renewal_date = models.DateField(blank=True, null=True)
    logo = models.ImageField(upload_to="uploads", blank=True, null=True)
    is_displayed = models.BooleanField(default=False)
    website_url = models.URLField(blank=True, null=True)

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
            self.contact_person, self.contact_email, self.prospective_sponsor, self.sponsor_level
        )
        self.update_details()

    def send_thank_you_email(self):
        send_thank_you_email(self.contact_person, self.contact_email)
        self.update_details()
