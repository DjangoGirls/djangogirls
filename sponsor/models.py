from django.db import models
from django.utils.translation import gettext_lazy as _


class Sponsor(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    logo = models.ImageField(
        upload_to="event/sponsors/",
        null=True,
        blank=True,
        help_text=_("Make sure logo is not bigger than 200 pixels wide"),
    )
    url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)

    def logo_display_for_admin(self):
        if self.logo:
            return f'<a href="{self.logo.url}" target="_blank"><img src="{self.logo.url}" width="100" /></a>'
        else:
            return _("No logo")

    logo_display_for_admin.allow_tags = True


class Donor(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    amount = models.FloatField()
    visible = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("amount",)
