from django.db import models
from django.utils.safestring import mark_safe

class StockPicture(models.Model):
    COVER = "CO"
    BACKGROUND = "BA"
    KIND_CHOICES = (
        (COVER, "Event cover (356 x 210px)"),
        (BACKGROUND, "Section background"),
    )

    photo = models.ImageField(upload_to="stock_pictures/")
    photo_credit = models.CharField(max_length=200,
        help_text=mark_safe(
            "Only use pictures with a "
            "<a href='https://creativecommons.org/licenses/'>Creative Commons license</a>."))
    photo_link = models.URLField("photo URL")
    kind = models.CharField(
        max_length=2,
        choices=KIND_CHOICES,
        blank=False
    )

    def __str__(self):
        return self.photo.name
