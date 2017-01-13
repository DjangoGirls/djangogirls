from django.template.loader import render_to_string

from core.emails import send_email


def send_application_confirmation(event_application):
    subject = (
        "Confirmation of application to organise Django Girls {} workshop"
        .format(event_application.city))
    content = render_to_string(
        'emails/organize/application_confirmation.html',
        {
            'city': event_application.city,
            'main_organizer_name': event_application.get_main_organizer_name()
        })
    send_email(content, subject, event_application.get_all_recipients())


def send_application_deployed_email(event_application, event, email_password):
    subject = (
        "Congrats! Your application to organize Django Girls {} "
        "has been accepted!".format(event_application.city))
    content = render_to_string('emails/organize/event_deployed.html', {
        'event': event,
        'password': email_password,
    })
    recipients = event_application.get_all_recipients()
    recipients.append(event.email)  # add event's djangogirls.org email
    send_email(content, subject, recipients)


def send_application_rejection_email(event_application):
    """ Sends a rejection email to all organizars who created this application
    """
    subject = (
        "Application to organize Django Girls {} has been reviewed"
        .format(event_application.city))
    content = render_to_string('emails/organize/rejection.html', {
        'application': event_application
    })
    send_email(content, subject, event_application.get_all_recipients())
