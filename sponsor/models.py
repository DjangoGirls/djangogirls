from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

EXTENSIONES_PERMITIDAS = ["png", "jpg", "jpeg", "gif", "webp", "svg"]

class Sponsor(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    logo = models.FileField(
        upload_to="event/sponsors/",
        null=True,
        blank=True,
        help_text=_("Asegurate de que el logo no supere los 200 píxeles de ancho. Formatos aceptados: PNG, JPG, GIF, WebP, SVG."),
        validators=[FileExtensionValidator(allowed_extensions=EXTENSIONES_PERMITIDAS)],
    )
    url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def logo_display_for_admin(self):
        if self.logo:
            return f'<a href="{self.logo.url}" target="_blank"><img src="{self.logo.url}" width="100" /></a>'
        else:
            return _("Sin logo")

    logo_display_for_admin.allow_tags = True