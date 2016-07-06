import click
import pytest

from django.core.management import call_command
from django.test import TestCase

from core.models import Event
from core.management.commands.add_organizer import Command


class CommandsTestCase(TestCase):
    fixtures = ['core_views_testdata.json']

    def setUp(self):
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


@pytest.mark.runner_setup(echo_stdin=True)
@pytest.mark.django_db
def test_cli(cli_runner):
    call_command('loaddata', 'core_views_testdata.json')

    event = Event.objects.get(pk=1)
    assert event.team.count() == 2

    command_input = (
        "1\n"
        "Jan Kowalski\n"
        "jan@kowalski.example\n"
        "N\n"
    )
    command = Command()
    result = cli_runner.invoke(
        command.handle,
        input=command_input
    )
    print(result)
    event = Event.objects.get(pk=1)
    print(event.team.all())
    assert event.team.count() == 3
