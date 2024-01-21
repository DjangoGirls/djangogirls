from django import forms
from models.event import Event
from models.organizer import OrganizerIssue
from models.user import User


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
            "last_updated",
        )
