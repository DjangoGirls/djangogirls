from django import forms
from tinymce.widgets import AdminTinyMCE


class EventPageContentForm(forms.ModelForm):

    class Meta:
        widgets = {
            'content': AdminTinyMCE()
        }
        fields = (
            'event',
            'name',
            'content',
            'background',
            'position',
            'is_public',
        )
