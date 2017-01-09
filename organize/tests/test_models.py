from django.core import mail
from django.core.exceptions import ValidationError
from django.test import TestCase

from organize.constants import DEPLOYED, ON_HOLD, REJECTED
from organize.models import EventApplication


class EventApplicationTest(TestCase):
    fixtures = ['event_application_testdata.json', "core_views_testdata.json"]

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

        event_application.status == REJECTED
        assert len(mail.outbox) == 1
        email = mail.outbox[0]
        assert email.to == event_application.get_organizers_emails()

    def test_deploy_event_from_previous_event(self):
        event_application = EventApplication.objects.get(pk=1)
        event_application.previous_event_id = 1
        event_application.save()

        event_application.deploy()

        event_application.status == DEPLOYED
        assert len(mail.outbox) == 4
        email_subjects = [e.subject for e in mail.outbox]
        self.assertTrue("Access to Django Girls website" in email_subjects)
        self.assertTrue("Congrats! Your application to organize Django Girls London has been accepted!" in email_subjects)