from django import forms

from core.models.event import Event
from core.models.organizerissue import OrganizerIssue
from core.models.user import User


class OrganizerIssueForm(forms.ModelForm):
    organizer = forms.ModelChoiceField(queryset=User.objects.all())
    event = forms.ModelChoiceField(queryset=Event.objects.all())
    issue_handled_by = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True))

    class Meta:
        model = OrganizerIssue
        fields = (
            "organizer",
            "event",
            "date_reported",
            "reported_by",
            "issue",
            "issue_handled",
            "issue_handled_by",
            "findings",
            "comments",
        )
