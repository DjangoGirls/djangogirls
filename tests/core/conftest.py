import pytest

from coach.models import Coach
from core.models import EventPageContent, EventPageMenu
from sponsor.models import Sponsor


@pytest.fixture()
def coach():
    return Coach.objects.create(
        name="Anna Smith")


@pytest.fixture()
def sponsor():
    return Sponsor.objects.create(
        name="Company name")


@pytest.fixture()
def past_event_page_content(past_event, coach, sponsor):
    coach_content = EventPageContent.objects.create(
        name="coach",
        content="<div><h2>Be a Mentor!</h2></div>",
        background="event/backgrounds/photo0_cBUZ8zp.jpg",
        is_public=True,
        position=40,
        event=past_event)
    coach_content.coaches.add(coach)
    sponsor_content = EventPageContent.objects.create(
        name="partners",
        content="<h3>Sponsors</h3>",
        background="",
        is_public=True,
        position=50,
        event=past_event)
    sponsor_content.sponsors.add(sponsor)


@pytest.fixture
def past_event_menu(past_event):
    EventPageMenu.objects.create(
        url="#values",
        position=1,
        event=past_event,
        title="About"
    )
    EventPageMenu.objects.create(
        url="#apply",
        position=10,
        event=past_event,
        title="Apply for a pass!"
    )
    EventPageMenu.objects.create(
        url="#faq",
        position=10,
        event=past_event,
        title="FAQ"
    )
