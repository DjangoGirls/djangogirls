from codemirror import CodeMirrorTextarea
from django import forms
from django.utils.safestring import mark_safe


class ResizableCodeMirror(CodeMirrorTextarea):

    def __init__(self, **kwargs):
        super().__init__(js_var_format='%s_editor', **kwargs)

    @property
    def media(self):
        mine = forms.Media(
            css={'all': ('vendor/jquery-ui/jquery-ui.min.css',)},
            js=('vendor/jquery-ui/jquery-ui.min.js',))
        return super().media + mine

    def render(self, name, value, attrs=None):
        output = super().render(name, value, attrs)
        return output + mark_safe(
            '''
                <script type="text/javascript">
                $('.CodeMirror').resizable({
                  resize: function() {
                    %s_editor.setSize($(this).width(), $(this).height());
                  }
                });
                </script>
            ''' % name
        )


class EventPageContentForm(forms.ModelForm):

    class Meta:
        widgets = {
            'content': ResizableCodeMirror(mode="xml")
        }
        fields = (
            'event',
            'name',
            'content',
            'background',
            'position',
            'is_public',
        )
