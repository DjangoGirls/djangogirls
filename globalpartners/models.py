from django.db import models

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
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    contact_email = models.EmailField(max_length=100)
    prospective_sponsor = models.BooleanField(default=False)
    patreon_sponsor = models.BooleanField(default=False)
    patreon_sponsor_level = models.CharField(max_length=20, blank=True, null=True, choices=PATREON_LEVELS)
    sponsor_level = models.CharField(max_length=20, blank=True, null=True, choices=ANNUAL_SPONSOR_LEVELS)
    date_joined = models.DateTimeField(blank=True, null=True)
    date_contacted = models.DateField(blank=True, null=True)
    next_renewal_date = models.DateTimeField(blank=True, null=True)
    logo = models.ImageField(upload_to="uploads")
    is_displayed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
