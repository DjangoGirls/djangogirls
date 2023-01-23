from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def notify_existing_user(user, event):
    """Sends e-mail to existing organizer, that they're added
    to the new Event.
    """
    content = render_to_string("emails/existing_user.html", {"user": user, "event": event})
    subject = "You have been granted access to new Django Girls event"
    send_email(content, subject, [user.email])


def notify_new_user(user, event, password, errors=None):
    """Sends e-mail to newly created organizer that their account was created
    and that they were added to the Event.
    """
    content = render_to_string(
        "emails/new_user.html",
        {
            "user": user,
            "event": event,
            "password": password,
            "errors": errors,
        },
    )
    subject = "Access to Django Girls website"
    send_email(content, subject, [user.email])


def send_email(content, subject, recipients, reply_to=None):
    msg = EmailMessage(subject, content, settings.DEFAULT_FROM_EMAIL, recipients, reply_to=reply_to)
    msg.content_subtype = "html"
    msg.send()
