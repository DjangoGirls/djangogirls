import random
from datetime import date

import pytest
import vcr
from click.testing import CliRunner
from django.core.management import call_command

from core.management.commands.add_organizer import command as add_organizer
from core.management.commands.copy_event import command as copy_event
from core.management.commands.new_event import command as new_event
from core.management.commands.prepare_dispatch import command as prepare_dispatch
from core.models import Event


@pytest.fixture
def click_runner():
    return CliRunner(echo_stdin=True)


@pytest.fixture
def random_day():
    today = date.today()
    start_date = today.toordinal()
    end_date = today.replace(year=today.year + 10).toordinal()
    random_day = date.fromordinal(random.randint(start_date, end_date))
    return random_day.strftime("%d/%m/%Y")


@vcr.use_cassette("tests/core/vcr/update_coordinates.yaml")
def test_update_coordinates(click_runner, past_event):
    latlng = past_event.latlng
    past_event.latlng = None
    past_event.save()

    past_event.refresh_from_db()
    assert past_event.latlng is None

    call_command("update_coordinates")

    past_event.refresh_from_db()
    assert past_event.latlng == latlng


def test_add_organizer(click_runner, future_event):
    assert future_event.team.count() == 1

    command_input = f"{future_event.pk}\n" "Jan Kowalski\n" "jan@kowalski.example.org\n" "N\n"

    click_runner.invoke(add_organizer, input=command_input, catch_exceptions=False)
    future_event.refresh_from_db()
    assert future_event.team.count() == 2


def test_new_event_with_one_organizer(click_runner, random_day, events, slack_mock, settings):
    settings.ENABLE_SLACK_NOTIFICATIONS = True
    assert Event.objects.count() == 4

    command_input = (
        "Oz\n" "Neverland\n" f"{random_day}\n" "oz\n" "oz\n" "Jan Kowalski\n" "jan@kowalski.example.org\n" "N\n"
    )

    click_runner.invoke(new_event, input=command_input, catch_exceptions=False)
    assert Event.objects.count() == 5
    event = Event.objects.order_by("pk").last()
    assert event.team.count() == 1
    slack_mock.chat_postMessage.assert_called_once()


def test_new_event_with_two_organizers(click_runner, random_day, events, slack_mock, settings):
    settings.ENABLE_SLACK_NOTIFICATIONS = True

    assert Event.objects.count() == 4

    command_input = (
        "Oz\n"
        "Neverland\n"
        f"{random_day}\n"
        "oz\n"
        "oz\n"
        "Jan Kowalski\n"
        "jan@kowalski.example.org\n"
        "Y\n"
        "Eleanor Organizer\n"
        "ealenor@organizer.example.org\n"
        "N"
    )

    click_runner.invoke(new_event, input=command_input, catch_exceptions=False)
    assert Event.objects.count() == 5
    event = Event.objects.order_by("pk").last()
    assert event.team.count() == 2
    slack_mock.chat_postMessage.assert_called_once()


def test_new_event_short(click_runner, random_day, events, stock_pictures, slack_mock, settings):
    settings.ENABLE_SLACK_NOTIFICATIONS = True

    assert Event.objects.count() == 4

    command_input = (
        "Oz\n" "Neverland\n" f"{random_day}\n" "oz\n" "oz\n" "Jan Kowalski\n" "jan@kowalski.example.org\n" "N\n"
    )

    result = click_runner.invoke(new_event, args=["--short"], input=command_input, catch_exceptions=False)
    assert Event.objects.count() == 5
    short_email_body = "Event e-mail is: oz@djangogirls.org\n" "Event website address is: https://djangogirls.org/oz"
    assert short_email_body in result.output
    slack_mock.chat_postMessage.assert_called_once()


def test_copy_event(click_runner, random_day, events, past_event):
    assert Event.objects.count() == 4

    new_event_number = 2
    command_input = f"{past_event.pk}\n" f"{new_event_number}\n" f"{random_day}\n"

    click_runner.invoke(copy_event, input=command_input, catch_exceptions=False)
    old_event = past_event
    name = old_event.name.split("#")[0].strip()
    new_name = f"{name} #{new_event_number}"
    try:
        new_event = Event.objects.get(name=new_name)
    except Event.DoesNotExist:
        pytest.fail("Event not copied properly!")

    assert new_event.city == old_event.city
    assert new_event.team.count() == old_event.team.count()

    assert new_event.page_main_color == old_event.page_main_color
    assert new_event.content.count() == old_event.content.count()
    assert new_event.menu.count() == old_event.menu.count()


def test_prepare_dispatch_with_data(click_runner):
    today = date.today()
    start_date = today.replace(year=today.year - 20).toordinal()
    end_date = today.toordinal()
    random_past_day = date.fromordinal(random.randint(start_date, end_date))

    command_input = f'{random_past_day.strftime("%Y-%m-%d")}\n'

    result = click_runner.invoke(prepare_dispatch, input=command_input, catch_exceptions=False)
    assert result.exception is None
    assert "PREVIOUS EVENTS" in result.output


def test_prepare_dispatch_without_data(click_runner):
    start_date = date.today().toordinal()
    random_past_day = date.fromordinal(random.randint(start_date, start_date))

    command_input = f'{random_past_day.strftime("%Y-%m-%d")}\n'

    result = click_runner.invoke(prepare_dispatch, input=command_input, catch_exceptions=False)
    assert result.exception is None
    assert "PREVIOUS EVENTS" in result.output


def test_prepare_dispatch_wrong_date(click_runner):
    start_date = date.today().toordinal()
    random_past_day = date.fromordinal(random.randint(start_date, start_date))

    command_input = f'{random_past_day.strftime("%Y/%m/%d")}\n'

    result = click_runner.invoke(prepare_dispatch, input=command_input)
    assert isinstance(result.exception, ValueError)
    assert "PREVIOUS EVENTS" not in result.output
