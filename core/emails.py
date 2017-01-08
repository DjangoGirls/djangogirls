from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def notify_existing_user(user, event):
    """ Sends e-mail to existing organizer, that they're added
        to the new Event.
    """
    content = render_to_string('emails/existing_user.html', {
        'user': user,
        'event': event
    })
    subject = 'You have been granted access to new Django Girls event'
    send_email(content, subject, [user.email])


def notify_new_user(user, event, password, errors=None):
    """ Sends e-mail to newly created organizer that their account was created
        and that they were added to the Event.
    """
    content = render_to_string('emails/new_user.html', {
        'user': user,
        'event': event,
        'password': password,
        'errors': errors,
    })
    subject = 'Access to Django Girls website'
    send_email(content, subject, [user.email])


def send_application_rejection_email(event_application):
    """ Sends a rejection email to all organizars who created this application
    """
    subject = "Application to organize Django Girls {} has been reviewed".format(event_application.city)
    content = render_to_string('emails/organize/rejection.html', {
        'application': event_application
    })
    send_email(content, subject, event_application.get_all_recipients())


def send_application_deployed_email(event_application, event, email_password):
    subject = "Congrats! Your application to organize Django Girls {} has been accepted!".format(
        event_application.city)
    content = render_to_string('emails/organize/event_deployed.html', {
        'event': event,
        'password': email_password,
    })
    recipients = event_application.get_all_recipients()
    recipients.append(event.email)  # add event's djangogirls.org email
    send_email(content, subject, recipients)


def send_email(content, subject, recipients):
    msg = EmailMessage(subject,
                       content,
                       settings.DEFAULT_FROM_EMAIL,
                       recipients)
    msg.content_subtype = "html"
    msg.send()
