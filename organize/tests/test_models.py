from django.core import mail
from django.core.exceptions import ValidationError
from django.test import TestCase

from organize.constants import ON_HOLD, REJECTED
from organize.models import EventApplication


class EventApplicationTest(TestCase):
    fixtures = ['event_application_testdata.json']

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
        assert len(event_application.get_all_recipients()) == \
            event_application.coorganizers.count() + 1

    def test_reject_method(self):
        event_application = EventApplication.objects.get(pk=1)
        event_application.reject()

        event_application.status == REJECTED
        assert len(mail.outbox) == 1
        email = mail.outbox[0]
        assert email.to == event_application.get_all_recipients()
