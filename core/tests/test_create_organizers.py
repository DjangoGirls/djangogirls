from unittest.mock import patch

from django.test import TestCase

from core.create_organizers import create_organizers
from core.models import Event
from organize.models import EventApplication


class CreateOrganizersTest(TestCase):
    fixtures = [
        'event_application_testdata.json',
        'core_views_testdata.json',
        'groups_testdata.json',
    ]

    @patch('core.models.user_invite')
    def test_create_organizers(self, mock_user_invite):
        event_application = EventApplication.objects.get(pk=1)
        event = Event.objects.get(pk=1)
        self.assertEquals(event.team.count(), 2)
        create_organizers(event, event_application, "fake_password")

        self.assertEquals(event.team.count(), 4)
        expected_emails = [
            "robert@test.com",
            "anna@test.com",
            "tinkerbell@gmail.com",
            "peterpan@example.com"
        ]
        self.assertEquals(
            set(expected_emails),
            set([e.email for e in event.team.all()])
        )
