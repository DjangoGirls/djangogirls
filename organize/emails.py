from django.template.loader import render_to_string

from core.emails import send_email


def send_application_confirmation(event_application):
    subject = f"Confirmation of application to organise Django Girls {event_application.city} workshop"
    content = render_to_string(
        "emails/organize/application_confirmation.html",
        {
            "city": event_application.city,
        },
    )
    send_email(content, subject, event_application.get_organizers_emails())


def send_application_notification(event_application):
    """
    Triggered when user submits application to organize new Django Girls event
    Sent to hello@djangogirls.org as a notification with reply-to to organizers
    who applied
    """
    subject = (
        f"New request to organise Django Girls {event_application.city}, {event_application.get_country_display()}"
    )
    content = render_to_string(
        "emails/organize/application_notification.html",
        {
            "application": event_application,
        },
    )
    send_email(content, subject, ["hello@djangogirls.org"], reply_to=[event_application.get_main_organizer_email()])


def send_application_deployed_email(event_application, event, email_password):
    subject = f"Congrats! Your application to organize Django Girls {event_application.city} has been accepted!"
    content = render_to_string(
        "emails/organize/event_deployed.html",
        {
            "event": event,
            "password": email_password,
        },
    )
    recipients = event_application.get_organizers_emails()
    recipients.append(event.email)  # add event's djangogirls.org email
    send_email(content, subject, recipients)


def send_application_rejection_email(event_application):
    """Sends a rejection email to all organizers who created this application"""
    subject = f"Application to organize Django Girls {event_application.city} has been reviewed"
    content = render_to_string("emails/organize/rejection.html", {"application": event_application})
    send_email(content, subject, event_application.get_organizers_emails())
