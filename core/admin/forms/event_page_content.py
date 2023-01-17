import tinymce
from django import forms
from tinymce.widgets import AdminTinyMCE


class EventPageContentForm(forms.ModelForm):
    class Meta:
        widgets = {
            "content": AdminTinyMCE(
                mce_attrs={
                    "plugins": tinymce.settings.DEFAULT_CONFIG["plugins"] + " | code",
                    "toolbar": tinymce.settings.DEFAULT_CONFIG["toolbar"] + " | code",
                },
            )
        }
        fields = (
            "event",
            "name",
            "content",
            "background",
            "position",
            "is_public",
        )
