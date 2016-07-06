from click.testing import CliRunner

from django.core.management import call_command
from django.test import TestCase

from core.models import Event
from core.management.commands.add_organizer import command


class CommandsTestCase(TestCase):
    fixtures = ['core_views_testdata.json']

    def setUp(self):
        self.event_1 = Event.objects.get(pk=1)  # In the future
        self.runner = CliRunner(echo_stdin=True)

    def test_update_coordinates(self):
        event_2 = Event.objects.get(pk=2)
        latlng = event_2.latlng
        event_2.latlng = None
        event_2.save()

        event_2 = Event.objects.get(pk=2)
        self.assertEqual(event_2.latlng, None)

        call_command('update_coordinates')

        event_2 = Event.objects.get(pk=2)
        self.assertEqual(event_2.latlng, latlng)

    def test_add_organizer(self):
        event = Event.objects.get(pk=1)
        assert event.team.count() == 2

        command_input = (
            "1\n"
            "Jan Kowalski\n"
            "jan@kowalski.example\n"
            "N\n"
        )

        self.runner.invoke(
            command,
            input=command_input
        )
        event = Event.objects.get(pk=1)
        assert event.team.count() == 3
