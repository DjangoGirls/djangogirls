import copy

import tinymce

from django import forms
from tinymce.widgets import AdminTinyMCE


default_tinymce_config = copy.deepcopy(tinymce.settings.DEFAULT_CONFIG)
default_tinymce_config['plugins'] += ' | code'
default_tinymce_config['toolbar'] += ' | code'


class EventPageContentForm(forms.ModelForm):

    class Meta:
        widgets = {
            'content': AdminTinyMCE(
                mce_attrs={
                    'plugins': default_tinymce_config['plugins'],
                    'toolbar': default_tinymce_config['toolbar'],
                },
            )
        }
        fields = (
            'event',
            'name',
            'content',
            'background',
            'position',
            'is_public',
        )
