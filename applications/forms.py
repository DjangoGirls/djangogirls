from django import forms

from .models import Application, Answer, Question, Score, EmailMessage


class ApplicationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        """
        The form here is programatically generated out of Question objects
        """

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
                choices = ((x, x) for x in question.choices.split(';'))
                options['choices'] = choices

            if question.question_type in ['paragraph', 'text']:
                self.fields[name] = forms.CharField(**options)
            elif question.question_type == 'choices':
                if question.is_multiple_choice:
                    options['widget'] = forms.CheckboxSelectMultiple
                    self.fields[name] = forms.MultipleChoiceField(**options)
                else:
                    options['widget'] = forms.RadioSelect
                    self.fields[name] = forms.ChoiceField(**options)

            if question.question_type == 'email':
                self.fields[name] = forms.EmailField(**options)

        self.fields['newsletter_optin'] = forms.ChoiceField(
            widget = forms.RadioSelect,
            label = 'Do you want to receive news from the Django Girls team?',
            help_text = 'No spam, pinky swear! Only helpful programming tips and '
                'latest news from Django Girls world. We sent this very rarely.',
            required = True,
            choices = (('yes','Yes please!'), ('no','No, thank you'))
        )


    def save(self, *args, **kwargs):
        form = kwargs.pop('form')
        application = Application.objects.create(form=form)

        for name in self.cleaned_data:
            question = None
            pk = name.replace('question_', '')
            value = self.cleaned_data[name]
            try:
                question = Question.objects.get(pk=pk, form=form)
            except (Question.DoesNotExist, ValueError):
                if name == 'newsletter_optin':
                    if value == 'yes':
                        application.newsletter_optin = True
                    else:
                        application.newsletter_optin = False
                    application.save()

            value = ', '.join(value) if type(value) == list else value

            if question:
                Answer.objects.create(
                    application=application,
                    question=question,
                    answer=value
                )

                if question.question_type == 'email':
                    application.email = value
                    application.save()


class ScoreForm(forms.ModelForm):

    class Meta:
        model = Score
        fields = ['score', 'comment']


class EmailMessageForm(forms.ModelForm):

    class Meta:
        model = EmailMessage
        fields = ['recipients_group', 'subject', 'text']
