"""Management command for handling of automatic emails.

This is run via a scheduled task every hour and checks if there are any emails that need sending.

"""
import logging
from smtplib import SMTPException

import djclick as click
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils import timezone

from core.models import Event


def send_event_emails(
    events,
    subject_template,
    plain_template,
    html_template,
    timestamp_field,
    email_type,
    ignore_approximate_events=False,
):
    """Send out any that need sending (thank yous, information request, ...)."""

    for event in events:
        # Some emails can only be sent if the event has a proper date set, ignore approximate dates in those cases.
        if ignore_approximate_events and event.date_is_approximate:
            continue

        recipients = list(set([event.email] + list(event.team.all().values_list("email", flat=True))))
        context = {
            "event": event,
            "settings": settings,
        }
        html_content = render_to_string(html_template, context)
        plain_content = render_to_string(plain_template, context)
        subject_content = render_to_string(subject_template, context)

        try:
            send_mail(
                subject=subject_content,
                message=plain_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipients,
                html_message=html_content,
            )
        except SMTPException:
            logging.exception("Couldn't send {} email to {}".format(email_type, "".join(recipients)))
        else:
            setattr(event, timestamp_field, timezone.now())
            event.save(update_fields=[timestamp_field])


def send_thank_you_emails():
    """Send thank you emails a day after the event happened."""
    send_event_emails(
        events=Event.objects.filter(
            is_on_homepage=True,
            date__lte=timezone.now() - timezone.timedelta(days=1),
            thank_you_email_sent__isnull=True,
        ),
        subject_template="emails/event_thank_you_subject.txt",
        plain_template="emails/event_thank_you.txt",
        html_template="emails/event_thank_you.html",
        timestamp_field="thank_you_email_sent",
        email_type="thank you email",
        ignore_approximate_events=True,
    )


def send_submit_information_emails():
    """Send "please provide numbers" emails.

    Happens if an event happened more than two weeks ago and has no statistics numbers yet.
    """
    events = Event.objects.filter(
        is_on_homepage=True,
        date__lte=timezone.now() - timezone.timedelta(weeks=2),
        submit_information_email_sent__isnull=True,
        attendees_count__isnull=True,
    )
    send_event_emails(
        events=events,
        subject_template="emails/submit_information_subject.txt",
        plain_template="emails/submit_information_email.txt",
        html_template="emails/submit_information_email.html",
        timestamp_field="submit_information_email_sent",
        email_type="submit information email",
        ignore_approximate_events=True,
    )


def send_offer_help_emails():
    """Send "do you need help?" emails to events.

    This sends emails to events that are in the future but less than 6 weeks away.
    Because of dates being approximate, we sometimes can't tell if an event in the current month
    has happened or not on the db-level. So we need to catch it while it's more than a month away.
    """
    events = Event.objects.filter(
        is_on_homepage=True,
        date__gt=timezone.now(),
        date__lte=timezone.now() + timezone.timedelta(weeks=6),
        created_at__lte=timezone.now() - timezone.timedelta(weeks=2),
        offer_help_email_sent__isnull=True,
    ).filter(Q(is_page_live=False) | Q(form=None))
    send_event_emails(
        events=events,
        subject_template="emails/offer_help_subject.txt",
        plain_template="emails/offer_help_email.txt",
        html_template="emails/offer_help_email.html",
        timestamp_field="offer_help_email_sent",
        email_type="offer help email",
    )

    if events:
        send_mail(
            subject="Check-in email summary",
            message="Hi there!\n Check-in emails were automatically send to events with no live website "
            "or application form open. If the organizers don't contact you back soon, you should "
            "remove those events from the events page:\n" + "\n".join(e.city for e in events),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["hello@djangogirls.org"],
        )


@click.command()
def command():
    """Find and send out scheduled emails that need sending."""
    send_thank_you_emails()
    send_submit_information_emails()
    send_offer_help_emails()
