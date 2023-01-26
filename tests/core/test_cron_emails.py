"""Tests for cron-emails sent out by the handle_emails management command."""
import pytest
from click.testing import CliRunner
from django.utils import timezone
from django_date_extensions.fields import ApproximateDate

from core.management.commands import handle_emails
from core.models import Event


@pytest.fixture
def click_runner():
    return CliRunner(echo_stdin=True)


@pytest.fixture
def send_kwargs():
    return {
        "subject_template": "emails/submit_information_subject.txt",
        "plain_template": "emails/submit_information_email.txt",
        "html_template": "emails/submit_information_email.html",
        "timestamp_field": "submit_information_email_sent",
        "email_type": "submit information email",
    }


def test_approximate_date_behaviour(mailoutbox, send_kwargs):
    """Test logic for the behaviour of skipping events with approximate dates.

    Events with approximate dates should be skipped if ignore_approximate_dates is True
    """

    # Create an event with an approximate date
    event = Event.objects.create(date=ApproximateDate(year=2017, month=1), email="approximate@djangogirls.org")
    send_kwargs["events"] = [event]

    # We're ignoring approximate dates, so no email should be sent
    send_kwargs["ignore_approximate_events"] = True
    handle_emails.send_event_emails(**send_kwargs)
    assert len(mailoutbox) == 0

    # Now we're not ignoring approximate dates, so a mail should be sent.
    send_kwargs["ignore_approximate_events"] = False
    handle_emails.send_event_emails(**send_kwargs)
    assert len(mailoutbox) == 1

    # Still ignoring approximate dates, but now the event date is fixed,
    # so a mail should be sent.
    event.date = timezone.datetime.now()
    event.save()
    handle_emails.send_event_emails(**send_kwargs)
    assert len(mailoutbox) == 2


def test_email_recipients(mailoutbox, send_kwargs, future_event, organizer_peter, organizer_julia):
    """All emails should go to event.email and all team members, but only once."""
    send_kwargs["events"] = [future_event]
    future_event.email = organizer_peter.email
    future_event.save()
    future_event.team.add(organizer_julia)

    handle_emails.send_event_emails(**send_kwargs)
    assert len(mailoutbox) == 1
    assert set(mailoutbox[0].to) == {organizer_peter.email, organizer_julia.email}


def test_email_template_rendering(mailoutbox, send_kwargs):
    """Test basic email rendering for templates and content."""
    city_name = "definitely not a city that will actually show up in a template"
    event = Event.objects.create(city=city_name, email="user-1@example.com")
    send_kwargs["events"] = [event]

    handle_emails.send_event_emails(**send_kwargs)

    assert len(mailoutbox) == 1
    mail = mailoutbox[0]
    html_content, _ = mail.alternatives[0]
    assert "<p>" in html_content
    assert "<p>" not in mail.body
    assert event.city in html_content


def test_thank_you_email_logic(mailoutbox):
    """Test event filtering logic for thank you emails."""
    should_be_included = Event.objects.create(
        city="should be included",
        is_on_homepage=True,
        date=timezone.now() - timezone.timedelta(days=1),
        email="first@djangogirls.org",
    )
    Event.objects.create(
        city="not on homepage",
        is_on_homepage=False,
        date=timezone.now() - timezone.timedelta(days=1),
        email="second@djangogirls.org",
    )
    Event.objects.create(
        city="in future",
        is_on_homepage=True,
        date=timezone.now() + timezone.timedelta(days=1),
        email="third@djangogirls.org",
    )
    Event.objects.create(
        city="already sent",
        is_on_homepage=True,
        date=timezone.now() - timezone.timedelta(days=1),
        thank_you_email_sent=timezone.now(),
        email="fourth@djangogirls.org",
    )

    handle_emails.send_thank_you_emails()

    # Only a single event should have been picked up
    assert len(mailoutbox) == 1
    assert should_be_included.city in mailoutbox[0].subject


def test_submit_information_email_logic(mailoutbox):
    """Test event filtering logic for thank you emails."""
    eight_weeks_ago = timezone.now() - timezone.timedelta(weeks=8)

    should_be_included = Event.objects.create(
        city="should be included", is_on_homepage=True, date=eight_weeks_ago, email="first@djangogirls.org"
    )
    Event.objects.create(
        city="not on homepage", is_on_homepage=False, date=eight_weeks_ago, email="second@djangogirls.org"
    )
    Event.objects.create(
        city="uncertain date",
        is_on_homepage=True,
        date=ApproximateDate(year=eight_weeks_ago.year, month=eight_weeks_ago.month),
        email="third@djangogirls.org",
    )
    Event.objects.create(
        city="data already provided",
        is_on_homepage=True,
        date=eight_weeks_ago,
        applicants_count=1,
        attendees_count=1,
        email="fourth@djangogirls.org",
    )
    Event.objects.create(
        city="already sent",
        is_on_homepage=True,
        date=eight_weeks_ago,
        submit_information_email_sent=timezone.now(),
        email="fifth@djangogirls.org",
    )

    handle_emails.send_submit_information_emails()

    # Only a single event should have been picked up
    assert len(mailoutbox) == 1
    assert should_be_included.city in mailoutbox[0].subject
