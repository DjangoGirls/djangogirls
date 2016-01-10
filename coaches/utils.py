from collections import OrderedDict
from django import forms


def generate_form_from_coach_questions(questions):
    fields = OrderedDict()

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
            fields[name] = forms.CharField(**options)
        elif question.question_type == 'choices':
            if question.is_multiple_choice:
                options['widget'] = forms.CheckboxSelectMultiple
                fields[name] = forms.MultipleChoiceField(**options)
            else:
                options['widget'] = forms.RadioSelect
                fields[name] = forms.ChoiceField(**options)

        if question.question_type == 'email':
            fields[name] = forms.EmailField(**options)

    return fields


def get_coach_applications_for_page(page, state=None, order=None):
    """
    Return a QuerySet of CoachApplication objects for a given page.
    Raises Form.DoesNotExist if Form for page does not yet exist.
    """
    from coaches.models import CoachForm  # circular import
    page_form = CoachForm.objects.filter(page=page)
    if not page_form.exists():
        raise CoachForm.DoesNotExist
    page_form = page_form.first()

    applications = page_form.coachapplication_set.all().order_by('id')

    if state:
        applications = applications.filter(state__in=state)

    if order:
        is_reversed = True if order[0] == '-' else False
        order = order[1:] if order[0] == '-' else order
        applications = sorted(applications, key=lambda app: getattr(app, order), reverse=is_reversed)

    return applications

DEFAULT_QUESTIONS = [
    {
        "title": "What's your name?",
        "question_type": "paragraph",
    },
    {
        "title": "Your e-mail address:",
        "question_type": "email",
    },
    {
        "title": "Your phone number:",
        "help_text": "Include your country prefix",
        "question_type": "paragraph",
    },
    {
        "title": "Which operating systems are you comfortable with?",
        "help_text": "As much as possible we would like to give you a group "
                     "that work on the same operating system as yours, so it's easier to help",
        "question_type": "choices",
        "choices": "Mac OS X; Windows; Linux",
        "is_multiple_choice": True,
    },
    {
        "title": "If we won't find a group suitable for your operating system are you willing to work with Windows?",
        "question_type": "choices",
        "choices": "Yes; No",
        "is_multiple_choice": False,
    },
    {
        "title": "With which group would you like to work the most?",
        "question_type": "choices",
        "choices": "Beginners; With basic HTML/CSS knowledge; With basic Python knowledge; I'm flexible",
        "is_multiple_choice": True,
    },
    {
        "title": "Please tell us a bit more about yourself",
        "help_text": "For example, why do you want to be a mentor? "
                     "What kind of work do you do? Have you coached before?",
        "question_type": "paragraph",
    },
    {
        "title": "Do you already know the tutorial at http://tutorial.djangogirls.org?",
        "question_type": "choices",
        "choices": "Yes; No, but I'll get familiar with it before the workshop",
    },
    {
        "title": "It is important that all coaches comply with the "
        "<a href='/pages/coc/'>Django Girls Code of Conduct</a>",
        "question_type": "choices",
        "choices": "I've read and understood the Django Girls Code of Conduct",
        "is_required": True,
        "is_multiple_choice": True,
    }
]
