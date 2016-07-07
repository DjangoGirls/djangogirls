from click.testing import CliRunner
from datetime import date
import random

from django.core.management import call_command
from django.test import TestCase

from core.models import Event
from core.management.commands.add_organizer import command as add_organizer
from core.management.commands.new_event import command as new_event


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
            add_organizer,
            input=command_input
        )
        event = Event.objects.get(pk=1)
        assert event.team.count() == 3

    def test_new_event_with_one_organizer(self):
        assert Event.objects.count() == 4

        today = date.today()
        start_date = today.toordinal()
        end_date = today.replace(year=today.year+10).toordinal()
        random_day = date.fromordinal(random.randint(start_date, end_date))

        command_input = (
            "Oz\n"
            "Neverland\n"
            "{random_day}\n"
            "oz\n"
            "oz@djangogirs.org\n"
            "Jan Kowalski\n"
            "jan@kowalski.example\n"
            "N\n"
        ).format(random_day=random_day.strftime("%d/%m/%Y"))

        self.runner.invoke(
            new_event,
            input=command_input
        )
        assert Event.objects.count() == 5
        event = Event.objects.last()
        assert event.team.count() == 1

    def test_new_event_with_two_organizers(self):
        assert Event.objects.count() == 4

        today = date.today()
        start_date = today.toordinal()
        end_date = today.replace(year=today.year+10).toordinal()
        random_day = date.fromordinal(random.randint(start_date, end_date))

        command_input = (
            "Oz\n"
            "Neverland\n"
            "{random_day}\n"
            "oz\n"
            "oz@djangogirs.org\n"
            "Jan Kowalski\n"
            "jan@kowalski.example\n"
            "Y\n"
            "Eleanor Organizer\n"
            "ealenor@organizer.extra\n"
            "N"
        ).format(random_day=random_day.strftime("%d/%m/%Y"))

        self.runner.invoke(
            new_event,
            input=command_input
        )
        assert Event.objects.count() == 5
        event = Event.objects.last()
        assert event.team.count() == 2
