from django.apps import AppConfig

from .utils import _monkeypatch_user_invite


class MonkeyPatchingConfig(AppConfig):
    name = 'slack_client'
    verbose_name = 'Slack Client'

    def ready(self):
        _monkeypatch_user_invite()
