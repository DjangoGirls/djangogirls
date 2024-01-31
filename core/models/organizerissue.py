from django.db import models

from core.models.event import Event
from core.models.user import User


class OrganizerIssue(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    organizer = models.ForeignKey(User, related_name="oganizer", on_delete=models.deletion.CASCADE)
    event = models.ForeignKey(to=Event, null=True, blank=True, related_name="event", on_delete=models.deletion.SET_NULL)
    date_reported = models.DateField()
    reported_by = models.CharField(max_length=100)
    reporter_email = models.EmailField(max_length=100)
    issue = models.TextField()
    issue_handled = models.BooleanField()
    issue_handled_by = models.ForeignKey(
        to=User, null=True, blank=True, related_name="staff_responsible", on_delete=models.deletion.SET_NULL
    )
    findings = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.organizer.get_full_name()} - {self.event}"

    def blacklist_organizer(self):
        user = User.objects.get(id=self.organizer.id)
        user.is_blacklisted = True
        user.save()

    def reverse_blacklist_organizer(self):
        user = User.objects.get(id=self.organizer.id)
        user.is_blacklisted = False
        user.save()
