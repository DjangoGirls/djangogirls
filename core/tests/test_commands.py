import builtins
import mock

from click.testing import CliRunner

from django.core.management import call_command
from django.test import TestCase

from core.models import Event


class CommandsTestCase(TestCase):
    fixtures = ['core_views_testdata.json']

    def setUp(self):
        self.runner = CliRunner()
        self.event_1 = Event.objects.get(pk=1)  # In the future

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

    # def test_add_organizer(self):
    #     " Test adding organizers to events"
    #     self.assertTrue(Event.objects.all(), 4)

    #     command_input = (
    #         "1\n",
    #         "Jan Kowalski\n",
    #         "jan@kowalski.example\n",
    #         "no\n",
    #     )
    #     input_generator = (i for i in command_input)
    #     with mock.patch.object(
    #         builtins, 'input',
    #         lambda prompt: next(input_generator)
    #     ):
    #         self.runner.invoke(
    #             call_command('add_organizer')
    #         )
