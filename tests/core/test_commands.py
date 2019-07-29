import random
from datetime import date
from unittest import mock

import pytest
import vcr
from click.testing import CliRunner
from django.core.management import call_command

from core.management.commands.prepare_dispatch import \
    command as prepare_dispatch
from core.models import Event

@pytest.fixture
def click_runner():
    return CliRunner(echo_stdin=True)


@pytest.fixture
def random_day():
    today = date.today()
    start_date = today.toordinal()
    end_date = today.replace(year=today.year+10).toordinal()
    random_day = date.fromordinal(random.randint(start_date, end_date))
    return random_day.strftime("%d/%m/%Y")


def test_prepare_dispatch_with_data(click_runner):
    today = date.today()
    start_date = today.replace(year=today.year-20).toordinal()
    end_date = today.toordinal()
    random_past_day = date.fromordinal(random.randint(start_date, end_date))

    command_input = (
        "{random_past_day}\n"
    ).format(random_past_day=random_past_day.strftime("%Y-%m-%d"))

    result = click_runner.invoke(
        prepare_dispatch,
        input=command_input
    )
    assert result.exception is None
    assert 'PREVIOUS EVENTS' in result.output


def test_prepare_dispatch_without_data(click_runner):
    start_date = date.today().toordinal()
    random_past_day = date.fromordinal(random.randint(start_date, start_date))

    command_input = (
        "{random_past_day}\n"
    ).format(random_past_day=random_past_day.strftime("%Y-%m-%d"))

    result = click_runner.invoke(prepare_dispatch, input=command_input)
    assert result.exception is None
    assert 'PREVIOUS EVENTS' in result.output


def test_prepare_dispatch_wrong_date(click_runner):
    start_date = date.today().toordinal()
    random_past_day = date.fromordinal(random.randint(start_date, start_date))

    command_input = (
        "{random_past_day}\n"
    ).format(random_past_day=random_past_day.strftime("%Y/%m/%d"))

    result = click_runner.invoke(prepare_dispatch, input=command_input)
    assert isinstance(result.exception, ValueError)
    assert 'PREVIOUS EVENTS' not in result.output
