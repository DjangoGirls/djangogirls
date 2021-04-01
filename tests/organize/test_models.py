import pytest
import vcr
from django.core.exceptions import ValidationError
from unittest import mock

from organize.constants import DEPLOYED, ON_HOLD, REJECTED
from core.models import Event


def test_comment_required_for_on_hold_application(base_application):
    base_application.clean()

    base_application.status = ON_HOLD
    with pytest.raises(ValidationError):
        base_application.clean()

    base_application.comment = "Comment"
    base_application.clean()


def test_all_recipients(application_with_coorganizer):
    emails = application_with_coorganizer.get_organizers_emails()
    assert len(emails) == application_with_coorganizer.coorganizers.count() + 1


def test_reject_method(base_application, mailoutbox):
    base_application.reject()

    assert base_application.status == REJECTED
    assert len(mailoutbox) == 1
    email = mailoutbox[0]
    assert email.to == base_application.get_organizers_emails()


@mock.patch('organize.models.gmail_accounts.get_or_create_gmail')
def test_deploy_event_from_previous_event(
        get_or_create_gmail, base_application, mailoutbox, stock_pictures):
    base_application.create_event()
    base_application.deploy()
    assert base_application.status == DEPLOYED


@mock.patch('organize.models.gmail_accounts.get_or_create_gmail')
def test_send_deployed_email(
        get_or_create_gmail, base_application, mailoutbox, stock_pictures):
    get_or_create_gmail.return_value = (
        '{}@djangogirls.org'.format(base_application.city),
        'asd123ASD')

    base_application.create_event()
    event = base_application.deploy()
    base_application.send_deployed_email(event)

    email_subjects = [e.subject for e in mailoutbox]
    assert len(mailoutbox) == 2
    assert "Access to Django Girls website" in email_subjects
    assert "Congrats! Your application to organize Django Girls London has been accepted!" in email_subjects


@vcr.use_cassette('tests/organize/vcr/latlng.yaml')
def test_latlng_is_fetched_when_creating_application(base_application):
    assert base_application.latlng == '0.0,0.0'
    base_application.latlng = ''
    base_application.save()
    assert base_application.latlng == '39.4747112, -0.3798074'


def test_has_past_team_members(organizer_peter, base_application):
    base_application.main_organizer_email = organizer_peter.email
    base_application.save()

    event = Event.objects.create(
        city=base_application.city,
        country=base_application.country,
    )

    # first event in city has nothing to compare so we return False
    assert not base_application.has_past_team_members(event)

    next_event = Event.objects.create(
        city=event.city,
        country=event.country
    )

    # if there are no same organizers we return False
    assert not base_application.has_past_team_members(next_event)

    event.team.add(organizer_peter)

    # if there is a common organizer, return True
    assert base_application.has_past_team_members(next_event)
