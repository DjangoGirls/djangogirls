import vcr
from django.core import mail
from django.core.exceptions import ValidationError
from django.test import TestCase

from organize.constants import DEPLOYED, ON_HOLD, REJECTED
from organize.models import EventApplication
from core.models import Event, User


class EventApplicationTest(TestCase):
    fixtures = [
        'event_application_testdata.json',
        'users_testdata.json',
        'pictures_testdata.json']

    def test_comment_required_for_on_hold_application(self):
        event_application = EventApplication.objects.get(pk=1)
        event_application.status = ON_HOLD
        with self.assertRaises(ValidationError):
            event_application.clean()

        event_application.comment = "Comment"
        try:
            event_application.clean()
        except ValidationError:
            self.fail("Event application should be valid.")

    def test_all_recipients(self):
        event_application = EventApplication.objects.get(pk=1)
        assert len(event_application.get_organizers_emails()) == \
            event_application.coorganizers.count() + 1

    def test_reject_method(self):
        event_application = EventApplication.objects.get(pk=1)
        event_application.reject()

        assert event_application.status == REJECTED
        assert len(mail.outbox) == 1
        email = mail.outbox[0]
        assert email.to == event_application.get_organizers_emails()

    @vcr.use_cassette('organize/tests/vcr/deploy_from_previous_event.yaml')
    def test_deploy_event_from_previous_event(self):
        event_application = EventApplication.objects.get(pk=1)
        event_application.create_event()
        event_application.deploy()

        assert event_application.status == DEPLOYED
        assert len(mail.outbox) == 4
        email_subjects = [e.subject for e in mail.outbox]
        self.assertTrue("Access to Django Girls website" in email_subjects)
        self.assertTrue("Congrats! Your application to organize Django Girls London has been accepted!" in email_subjects)

    @vcr.use_cassette('organize/tests/vcr/latlng.yaml')
    def test_latlng_is_fetched_when_creating_application(self):
        event_application = EventApplication.objects.get(pk=1)
        assert event_application.latlng == '0.0,0.0'
        event_application.latlng = ''
        event_application.save()
        assert event_application.latlng == '39.4747112, -0.3798073'

    def test_has_past_team_members(self):
        user = User.objects.get(pk=1)
        event_application = EventApplication.objects.get(pk=1)
        event_application.main_organizer_email = user.email
        event_application.save()

        event = Event.objects.create(
            city=event_application.city,
            country=event_application.country,
        )

        # first event in city has nothing to compare so we return False
        self.assertFalse(event_application.has_past_team_members(event))

        next_event = Event.objects.create(
            city=event.city,
            country=event.country
        )

        # if there are no same organizers we return False
        self.assertFalse(event_application.has_past_team_members(next_event))

        event.team.add(user)

        # if there is a common organizer, return True
        self.assertTrue(event_application.has_past_team_members(next_event))
