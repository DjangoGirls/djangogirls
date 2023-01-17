from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PatreonManagerConfig(AppConfig):
    name = "patreonmanager"
    verbose_name = _("Patreon Manager")
