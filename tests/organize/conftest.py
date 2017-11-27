import pytest

from organize.constants import ON_HOLD
from organize.models import EventApplication, Coorganizer


@pytest.fixture
def base_application():
    return EventApplication.objects.create(
        date="2080-10-10",
        city="London",
        country="Country",
        latlng='0.0,0.0',
        main_organizer_email="test@example.com",
        main_organizer_first_name="Anna",
        main_organizer_last_name="Smith")


@pytest.fixture
def application_with_coorganizer(base_application):
    Coorganizer.objects.create(
        event_application=base_application,
        email="anna@example.com",
        first_name="Anna",
        last_name="Smith")
    return base_application


@pytest.fixture
def application_on_hold(base_application):
    base_application.status = ON_HOLD
    base_application.save()

    return base_application