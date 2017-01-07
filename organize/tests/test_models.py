from django.core.exceptions import ValidationError
from django.test import TestCase

from organize.constants import ON_HOLD, REJECTED
from organize.models import EventApplication


class EventApplicationTest(TestCase):
    fixtures = ['organize_testdata.json']

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

    def test_rejection_reason_required_for_rejected_application(self):
        event_application = EventApplication.objects.get(pk=1)
        event_application.status = REJECTED
        with self.assertRaises(ValidationError):
            event_application.clean()

        event_application.rejection_reason = "Rejection reason"
        try:
            event_application.clean()
        except ValidationError:
            self.fail("Event application should be valid.")
