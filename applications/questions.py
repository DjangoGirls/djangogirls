from collections import OrderedDict

from django import forms
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def get_organiser_menu(page_url):
    """
    Get menu entries for organiser-visible pages
    """
    menu = [
        {"title": _("Applications"), "url": reverse("applications:applications", args=[page_url])},
        {"title": _("Messaging"), "url": reverse("applications:communication", args=[page_url])},
    ]

    return menu


def generate_form_from_questions(questions):
    fields = OrderedDict()

    for question in questions:
        options = {
            "label": question.title,
            "help_text": question.help_text or None,
            "required": question.is_required,
        }
        name = f"question_{question.pk}"

        if question.question_type == "text":
            options["widget"] = forms.Textarea

        if question.question_type == "choices":
            choices = ((x, x) for x in question.choices.split(";"))
            options["choices"] = choices

        if question.question_type in ["paragraph", "text"]:
            fields[name] = forms.CharField(**options)
        elif question.question_type == "choices":
            if question.is_multiple_choice:
                options["widget"] = forms.CheckboxSelectMultiple
                fields[name] = forms.MultipleChoiceField(**options)
            else:
                options["widget"] = forms.RadioSelect
                fields[name] = forms.ChoiceField(**options)

        if question.question_type == "email":
            fields[name] = forms.EmailField(**options)

    fields["newsletter_optin"] = forms.ChoiceField(
        widget=forms.RadioSelect,
        label=_("Do you want to receive news from the Django Girls team?"),
        help_text=_(
            "No spam, pinky swear! Only helpful programming tips and "
            "latest news from the Django Girls world. We send it once every two weeks."
        ),
        required=True,
        choices=(("yes", _("Yes, please!")), ("no", _("No, thank you."))),
    )

    return fields


DEFAULT_QUESTIONS = [
    {
        "title": _("What's your name?"),
        "question_type": "paragraph",
    },
    {
        "title": _("Your e-mail address:"),
        "question_type": "email",
    },
    {
        "title": _("Your phone number:"),
        "help_text": _("Include your country prefix"),
        "question_type": "paragraph",
    },
    {
        "title": _("Where are you from?"),
        "help_text": _("City, Country"),
        "question_type": "paragraph",
    },
    {
        "title": _("How old are you?"),
        "question_type": "paragraph",
        "is_required": False,
    },
    {
        "title": _("Which operating system do you use?"),
        "question_type": "choices",
        "choices": "Mac OS X; Windows; Linux",
        "is_multiple_choice": True,
    },
    {
        "title": _("What is your current level of experience with programming?"),
        "question_type": "choices",
        "choices": _(
            "I'm a total beginner, I don't know anything about it; "
            "I've tried some HTML or CSS before; I've tried some JavaScript "
            "before; I've done a few lessons of Python; I've built a website "
            "before; I work as a programmer"
        ),
        "is_multiple_choice": True,
    },
    {
        "title": _(
            "If you checked anything other than beginner, could you "
            "tell us a bit more about your programming knowledge?"
        ),
        "question_type": "text",
        "is_required": False,
    },
    {
        "title": _("What is your current occupation?"),
        "help_text": _("What is your current job? Are you a student?"),
        "question_type": "text",
    },
    {
        "title": _("Why do you want to attend the workshop?"),
        "help_text": _("Tell us about your motivations and aspirations."),
        "question_type": "text",
    },
    {
        "title": _("How are you planning to share what you've learnt with others?"),
        "help_text": _(
            "Django Girls is a volunteer-run organisation and we "
            "look for people who are active and can help us help more women get "
            "into the field. We want you to share what you learn at the workshop "
            "with others in different ways: by organising a Django Girls event "
            "in your city, talking about Django Girls on your local meetups, "
            "writing a blog or simply teaching your friends."
        ),
        "question_type": "text",
        "is_required": False,
    },
    {
        "title": _("How did you hear about Django Girls?"),
        "question_type": "choices",
        "choices": "; ".join(["Facebook", "Twitter", "From a friend", "PyLadies"]),
        "is_required": False,
        "is_multiple_choice": True,
    },
    {
        "title": _("I acknowledge that some of my data will be used on Third Party Sites and Services."),
        "help_text": _(
            "Data collected through this form is used only for the "
            "purpose of Django Girls events. We're using Third Party Sites "
            "and Services to make it happen: for example, we're using "
            "Sendgrid to send you emails. Don't worry: We don't share your data with spammers, "
            "and we don't sell it! More info on our Privacy policy "
            "<a href='/privacy-cookies/'>here</a>."
        ),
        "question_type": "choices",
        "choices": _("Yes"),
        "is_required": True,
        "is_multiple_choice": True,
    },
    {
        "title": _(
            "It is important that all attendees comply with the " "<a href='/coc/'>Django Girls Code of Conduct</a>"
        ),
        "question_type": "choices",
        "choices": _("I've read and understood the Django Girls Code of Conduct"),
        "is_required": True,
        "is_multiple_choice": True,
    },
]
