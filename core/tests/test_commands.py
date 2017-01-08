import random
from datetime import date

import vcr
from click.testing import CliRunner
from django.core.management import call_command
from django.test import TestCase

from core.management.commands.add_organizer import command as add_organizer
from core.management.commands.copy_event import command as copy_event
from core.management.commands.new_event import command as new_event
from core.management.commands.prepare_dispatch import \
    command as prepare_dispatch
from core.models import Event


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

    @vcr.use_cassette('core/tests/vcr/update_coordinates.yaml')
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
            "jan@kowalski.example.org\n"
            "N\n"
        )

        self.runner.invoke(
            add_organizer,
            input=command_input
        )
        event = Event.objects.get(pk=1)
        assert event.team.count() == 3

    @vcr.use_cassette('core/tests/vcr/new_event_with_one_organizer.yaml')
    def test_new_event_with_one_organizer(self):
        assert Event.objects.count() == 4

        random_day = self._get_random_day()

        command_input = (
            "Oz\n"
            "Neverland\n"
            "{random_day}\n"
            "oz\n"
            "oz\n"
            "Jan Kowalski\n"
            "jan@kowalski.example.org\n"
            "N\n"
        ).format(random_day=random_day.strftime("%d/%m/%Y"))

        self.runner.invoke(
            new_event,
            input=command_input
        )
        assert Event.objects.count() == 5
        event = Event.objects.order_by('pk').last()
        assert event.team.count() == 1

    @vcr.use_cassette('core/tests/vcr/new_event_with_two_organizers.yaml')
    def test_new_event_with_two_organizers(self):
        assert Event.objects.count() == 4

        random_day = self._get_random_day()

        command_input = (
            "Oz\n"
            "Neverland\n"
            "{random_day}\n"
            "oz\n"
            "oz\n"
            "Jan Kowalski\n"
            "jan@kowalski.example.org\n"
            "Y\n"
            "Eleanor Organizer\n"
            "ealenor@organizer.example.org\n"
            "N"
        ).format(random_day=random_day.strftime("%d/%m/%Y"))

        self.runner.invoke(
            new_event,
            input=command_input
        )
        assert Event.objects.count() == 5
        event = Event.objects.order_by('pk').last()
        assert event.team.count() == 2

    @vcr.use_cassette('core/tests/vcr/new_event_short.yaml')
    def test_new_event_short(self):
        assert Event.objects.count() == 4

        random_day = self._get_random_day()

        command_input = (
            "Oz\n"
            "Neverland\n"
            "{random_day}\n"
            "oz\n"
            "oz\n"
            "Jan Kowalski\n"
            "jan@kowalski.example.org\n"
            "N\n"
        ).format(random_day=random_day.strftime("%d/%m/%Y"))

        result = self.runner.invoke(
            new_event,
            args=["--short"],
            input=command_input
        )
        assert Event.objects.count() == 5
        short_email_body = """Event e-mail is: oz@djangogirls.org
Event website address is: http://djangogirls.org/oz"""
        assert short_email_body in result.output

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
        name = old_event.name.split('#')[0].strip()
        new_name = "{} #{}".format(name, new_event_number)
        try:
            new_event = Event.objects.get(name=new_name)
        except Event.DoesNotExist:
            self.fail("Event not copied properly!")

        assert new_event.city == old_event.city
        assert new_event.team.count() == old_event.team.count()

        assert new_event.page_main_color == old_event.page_main_color
        assert new_event.content.count() == old_event.content.count()
        assert new_event.menu.count() == old_event.menu.count()

    def test_prepare_dispatch_with_data(self):
        today = date.today()
        start_date = today.replace(year=today.year-20).toordinal()
        end_date = today.toordinal()
        random_past_day = date.fromordinal(
            random.randint(start_date, end_date))

        command_input = (
            "{random_past_day}\n"
        ).format(random_past_day=random_past_day.strftime("%Y-%m-%d"))

        result = self.runner.invoke(
            prepare_dispatch,
            input=command_input
        )
        assert result.exception is None
        assert b'PREVIOUS EVENTS' in result.output_bytes

    def test_prepare_dispatch_without_data(self):
        start_date = date.today().toordinal()
        random_past_day = date.fromordinal(
            random.randint(start_date, start_date))

        command_input = (
            "{random_past_day}\n"
        ).format(random_past_day=random_past_day.strftime("%Y-%m-%d"))

        result = self.runner.invoke(
            prepare_dispatch,
            input=command_input
        )
        assert result.exception is None
        assert b'PREVIOUS EVENTS' in result.output_bytes

    def test_prepare_dispatch_wrong_date(self):
        start_date = date.today().toordinal()
        random_past_day = date.fromordinal(
            random.randint(start_date, start_date))

        command_input = (
            "{random_past_day}\n"
        ).format(random_past_day=random_past_day.strftime("%Y/%m/%d"))

        result = self.runner.invoke(
            prepare_dispatch,
            input=command_input
        )
        assert isinstance(result.exception, ValueError)
        assert b'PREVIOUS EVENTS' not in result.output_bytes
