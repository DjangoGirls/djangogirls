from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.urlresolvers import reverse
from django.db import models

from easy_thumbnails.exceptions import InvalidImageFormatError
from easy_thumbnails.files import get_thumbnailer


DEFAULT_COACH_PHOTO = static('img/global/coach-empty.jpg')


class Coach(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    twitter_handle = models.CharField(
        max_length=200, null=True, blank=True,
        help_text="No @, No http://, just username")
    photo = models.ImageField(
        upload_to="event/coaches/", null=True, blank=True,
        help_text="For best display keep it square")
    url = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Coaches"

    def __str__(self):
        return self.name

    def photo_display_for_admin(self):
        coach_change_url = reverse("admin:coach_coach_change", args=[self.id])
        return """
            <a href=\"{}\" target=\"_blank\">
                <img src=\"{}\" width=\"100\" />
            </a>""".format(coach_change_url, self.photo_url)
    photo_display_for_admin.allow_tags = True

    @property
    def photo_url(self):
        if self.photo:
            try:
                return get_thumbnailer(self.photo)['coach'].url
            except InvalidImageFormatError:
                return DEFAULT_COACH_PHOTO

        return DEFAULT_COACH_PHOTO
