import pytest
from django.utils import timezone
from django_date_extensions.fields import ApproximateDate

from applications.models import Form
from core.management.commands import handle_emails
from core.models import Event


@pytest.fixture()
def event():
    in_six_weeks = timezone.now() + timezone.timedelta(weeks=6)

    return Event.objects.create(
        city="Test City", is_on_homepage=True, date=in_six_weeks, is_page_live=True, email="first@djangogirls.org"
    )


def test_event_in_six_weeks_emails_not_sent(event, mailoutbox):
    handle_emails.send_offer_help_emails()
    assert len(mailoutbox) == 0


def test_event_older_than_a_week_email_sent(event, mailoutbox):
    event.created_at = timezone.now() - timezone.timedelta(weeks=3)
    event.save()
    handle_emails.send_offer_help_emails()
    assert len(mailoutbox) == 2  # it's 2 because the second one goes to hello@
    assert event.city in mailoutbox[0].subject


def test_event_approx_in_future_email_sent(event, mailoutbox):
    event.created_at = timezone.now() - timezone.timedelta(weeks=3)

    in_six_weeks = timezone.now() + timezone.timedelta(weeks=6)
    event.date = ApproximateDate(year=in_six_weeks.year, month=in_six_weeks.month)
    event.save()
    handle_emails.send_offer_help_emails()
    assert len(mailoutbox) == 2  # it's 2 because the second one goes to hello@
    assert event.city in mailoutbox[0].subject


def test_event_past_start_date_email_not_sent(event, mailoutbox):
    event.date = timezone.now() - timezone.timedelta(days=1)
    event.save()
    handle_emails.send_offer_help_emails()
    assert len(mailoutbox) == 0


def test_event_date_uncertain_email_not_sent(event, mailoutbox):
    now = timezone.now()
    event.date = ApproximateDate(year=now.year, month=now.month)
    event.save()
    handle_emails.send_offer_help_emails()
    assert len(mailoutbox) == 0


def test_event_with_form_email_not_sent(event, mailoutbox):
    in_six_weeks = timezone.now() + timezone.timedelta(weeks=6)
    event.date = in_six_weeks
    event.save()
    Form.objects.create(event=event)
    handle_emails.send_offer_help_emails()
    assert len(mailoutbox) == 0


def test_event_page_not_live_email_not_sent(event, mailoutbox):
    event.is_page_live = False
    event.save()
    handle_emails.send_offer_help_emails()
    assert len(mailoutbox) == 0


def test_event_page_not_on_homepage_email_not_sent(event, mailoutbox):
    event.is_on_homepage = False
    event.save()
    handle_emails.send_offer_help_emails()
    assert len(mailoutbox) == 0


def test_send_summary_checkin_to_hello(event, mailoutbox):
    event.created_at = timezone.now() - timezone.timedelta(weeks=3)
    event.save()
    handle_emails.send_offer_help_emails()

    assert len(mailoutbox) == 2
    assert mailoutbox[0].to == [event.email]
    assert mailoutbox[1].to == ["hello@djangogirls.org"]
    assert event.city in mailoutbox[0].body
    assert mailoutbox[1].subject == "Check-in email summary"
