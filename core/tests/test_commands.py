from click.testing import CliRunner
from datetime import date
import random

from django.core.management import call_command
from django.test import TestCase

from core.models import Event
from core.management.commands.add_organizer import command as add_organizer
from core.management.commands.new_event import command as new_event
from core.management.commands.copy_event import command as copy_event


class CommandsTestCase(TestCase):
    fixtures = ['core_views_testdata.json']

    def setUp(self):
        self.event_1 = Event.objects.get(pk=1)  # In the future
        self.runner = CliRunner(echo_stdin=True)
        today = date.today()
        self.start_date = today.toordinal()
        self.end_date = today.replace(year=today.year+10).toordinal()

    def _get_random_day(self):
        return date.fromordinal(random.randint(self.start_date, self.end_date))

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

        random_day = self._get_random_day()

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

        random_day = self._get_random_day()

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

    def test_copy_event(self):
        assert Event.objects.count() == 4

        random_day = self._get_random_day()
        new_event_number = 2
        command_input = (
            "2\n"
            "{new_event_number}\n"
            "{random_day}\n"
        ).format(random_day=random_day.strftime("%d/%m/%Y"),
                 new_event_number=new_event_number)

        self.runner.invoke(
            copy_event,
            input=command_input
        )
        old_event = Event.objects.get(pk=2)
        old_eventpage = old_event.eventpage
        name = old_event.name.split('#')[0].strip()
        new_name = "{} #{}".format(name, new_event_number)
        try:
            new_event = Event.objects.get(name=new_name)
            new_eventpage = new_event.eventpage
        except Event.DoesNotExist:
            self.fail("Event not copied properly!")

        assert new_event.city == old_event.city
        assert new_event.team.count() == old_event.team.count()

        assert new_eventpage.main_color == old_eventpage.main_color
        assert new_eventpage.content.count() == old_eventpage.content.count()
        assert new_eventpage.menu.count() == old_eventpage.menu.count()
