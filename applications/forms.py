from django import forms


class ApplicationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super(ApplicationForm, self).__init__(*args, **kwargs)

        for question in questions:
            options = {
                'label': question.title,
                'help_text': question.help_text or None,
                'required': question.is_required,
            }
            name = 'question_{}'.format(question.pk)

            if question.question_type == 'text':
                options['widget'] = forms.Textarea

            if question.question_type == 'choices':
                options['choices'] = ((x, x) for x in question.choices.split(';'))

            if question.question_type in ['paragraph', 'text']:
                self.fields[name] = forms.CharField(**options)
            elif question.question_type == 'choices':
                if question.is_multiple_choice:
                    options['widget'] = forms.CheckboxSelectMultiple
                    self.fields[name] = forms.MultipleChoiceField(**options)
                else:
                    options['widget'] = forms.RadioSelect
                    self.fields[name] = forms.ChoiceField(**options)
