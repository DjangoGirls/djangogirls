import random

from django.db import models
from django.utils.functional import lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

mark_safe_lazy = lazy(mark_safe, str)


class EventPictureManager(models.Manager):
    def random_cover(self):
        queryset = self.get_queryset()
        return random.choice(queryset.filter(kind=StockPicture.COVER))

    def random_background(self):
        queryset = self.get_queryset()
        return random.choice(queryset.filter(kind=StockPicture.BACKGROUND))


class StockPicture(models.Model):
    COVER = "CO"
    BACKGROUND = "BA"
    KIND_CHOICES = (
        (COVER, _("Event cover (356 x 210px)")),
        (BACKGROUND, _("Section background")),
    )

    photo = models.ImageField(upload_to="stock_pictures/")
    photo_credit = models.CharField(
        max_length=200,
        help_text=mark_safe_lazy(
            _(
                "Only use pictures with a "
                "<a href='https://creativecommons.org/licenses/'>Creative Commons license</a>."
            )
        ),
    )
    photo_link = models.URLField(_("photo URL"))
    kind = models.CharField(max_length=2, choices=KIND_CHOICES)

    objects = EventPictureManager()

    def __str__(self):
        return self.photo.name
