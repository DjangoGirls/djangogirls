from django.db import models
from django.utils import timezone


class EventApplicationQuerySet(models.QuerySet):
    def change_status_to(self, status):
        """Same signature as EventApplication.change_status_to"""
        self.update(status=status, status_changed_at=timezone.now())
