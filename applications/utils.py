from django import forms


def generate_form_from_questions(questions):
    fields = {}

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

    fields['newsletter_optin'] = forms.ChoiceField(
        widget=forms.RadioSelect,
        label='Do you want to receive news from the Django Girls team?',
        help_text='No spam, pinky swear! Only helpful programming tips and '
            'latest news from Django Girls world. We sent this very rarely.',
        required=True,
        choices=(('yes', 'Yes please!'), ('no', 'No, thank you'))
    )

    return fields


def get_applications_for_page(page, state=None, rsvp_status=None, order=None):
    """
    Return a QuerySet of Application objects for a given page.
    Raises Form.DoesNotExist if Form for page does not yet exist.
    """
    from applications.models import Form  # circular import
    page_form = Form.objects.filter(page=page)
    if not page_form.exists():
        raise Form.DoesNotExist
    page_form = page_form.first()

    applications = page_form.application_set.all()

    if rsvp_status:
        applications = applications.filter(state='accepted', rsvp_status__in=rsvp_status)
    elif state:
        applications = applications.filter(state__in=state)

    if order:
        is_reversed = True if order[0] == '-' else False
        order = order[1:] if order[0] == '-' else order
        if order == 'average_score':
            # here is an exception for the average_score, because we also want to get
            # the standard deviation into account in this sorting
            applications = sorted(applications, key=lambda app: (getattr(app, order), -app.stdev()), reverse=is_reversed)
        else:
            applications = sorted(applications, key=lambda app: getattr(app, order), reverse=is_reversed)

    return applications


def random_application(request, page, prev_application):
    """
    Get a new random application for a particular event,
    that hasn't been scored by the request user.
    """
    from applications.models import Application  # circular import
    return Application.objects.filter(
        form__page=page
        ).exclude(pk=prev_application.id
        ).exclude(scores__user=request.user).order_by('?').first()


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
        "title": "Where are you from?",
        "help_text": "City, Country",
        "question_type": "paragraph",
    },
    {
        "title": "How old are you?",
        "question_type": "paragraph",
        "is_required": False,
    },
    {
        "title": "Which operating system do you use?",
        "question_type": "choices",
        "choices": "Mac OS X; Windows; Linux",
        "is_multiple_choice": True,
    },
    {
        "title": "What is your current level of experience with programming?",
        "question_type": "choices",
        "choices": "I'm a total beginner, I don't know anything about it; "
        "I've tried some HTML or CSS before; I've tried some JavaScript "
        "before; I've done a few lessons of Python; I've built a website "
        "before; I work as a programmer",
        "is_multiple_choice": True,
    },
    {
        "title": "If you checked anything other than beginner, could you "
        "tell us a bit more about your programming knowledge?",
        "question_type": "text",
        "is_required": False,
    },
    {
        "title": "What is your current occupation?",
        "help_text": "What is your current job? Are you a student?",
        "question_type": "text",
    },
    {
        "title": "Why do you want to attend the workshop?",
        "help_text": "Tell us about your motivations and aspirations.",
        "question_type": "text",
    },
    {
        "title": "How are you planning to share what you've learnt with "
        "others?",
        "help_text": "Django Girls is a volunteer-run organisation and we "
        "look for people who are active and can help us help more women get "
        "into the field. We want you to share what you learn at the workshop "
        "with others in different ways: by organising a Django Girls event "
        "in your city, talking about Django Girls on your local meetups, "
        "writing a blog or simply teaching your friends.",
        "question_type": "text",
        "is_required": False
    },
    {
        "title": "How did you hear about Django Girls?",
        "help_text": "Django Girls is a volunteer-run organisation and we "
        "look for people who are active and can help us help more women get "
        "into the field. We want you to share what you learn at the workshop "
        "with others in different ways: by organising a Django Girls event "
        "in your city, talking about Django Girls on your local meetups, "
        "writing a blog or simply teaching your friends.",
        "question_type": "choices",
        "choices": "Facebook; Twitter; From a friend; PyLadies",
        "is_required": False,
        "is_multiple_choice": True,
    },
    {
        "title": "It is important that all attendees comply with the "
        "<a href='/pages/coc/'>Django Girls Code of Conduct</a>",
        "question_type": "choices",
        "choices": "I've read and understood the Django Girls Code of Conduct",
        "is_required": True,
        "is_multiple_choice": True,
    }
]