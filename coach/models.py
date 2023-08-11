from django.core.exceptions import ValidationError
from django.db import IntegrityError, models
from django.templatetags.static import static
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.exceptions import InvalidImageFormatError
from easy_thumbnails.files import get_thumbnailer

DEFAULT_COACH_PHOTO = static("img/global/coach-empty.jpg")


class Coach(models.Model):
    name = models.CharField(max_length=200)
    twitter_handle = models.CharField(
        max_length=200, null=True, blank=True, help_text=_("No @, No http://, just username")
    )
    photo = models.ImageField(
        upload_to="event/coaches/", null=True, blank=True, help_text=_("For best display keep it square")
    )
    url = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = _("Coaches")
        unique_together = ["name", "twitter_handle"]

    def __str__(self):
        return self.name

    def photo_display_for_admin(self):
        coach_change_url = reverse("admin:coach_coach_change", args=[self.id])
        return f"""
            <a href=\"{coach_change_url}\" target=\"_blank\">
                <img src=\"{self.photo_url}\" width=\"100\" />
            </a>"""

    photo_display_for_admin.allow_tags = True

    @property
    def photo_url(self):
        if self.photo:
            try:
                return get_thumbnailer(self.photo)["coach"].url
            except InvalidImageFormatError:
                return DEFAULT_COACH_PHOTO

        return DEFAULT_COACH_PHOTO

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            raise ValidationError(
                {"name": _(f"Coach with name {self.name} and twitter_handle {self.twitter_handle} " "already exists.")}
            )
        return self
