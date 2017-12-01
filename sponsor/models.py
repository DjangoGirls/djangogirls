from django.db import models


class Sponsor(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    logo = models.ImageField(
        upload_to="event/sponsors/", null=True, blank=True,
        help_text="Make sure logo is not bigger than 200 pixels wide"
    )
    url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)

    def logo_display_for_admin(self):
        if self.logo:
            return "<a href=\"{}\" target=\"_blank\"><img src=\"{}\" width=\"100\" /></a>".format(
                self.logo.url, self.logo.url)
        else:
            return "No logo"

    logo_display_for_admin.allow_tags = True
