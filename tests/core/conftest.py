import pytest

from coach.models import Coach
from core.models import Event, EventPageContent, EventPageMenu
from globalpartners.models import GlobalPartner
from sponsor.models import Sponsor
from story.models import Story


@pytest.fixture()
def coach():
    return Coach.objects.create(name="Anna Smith")


@pytest.fixture()
def sponsor():
    return Sponsor.objects.create(name="Company name")


@pytest.fixture()
def past_event_page_content(past_event, coach, sponsor):
    coach_content = EventPageContent.objects.create(
        name="coach",
        content="<div><h2>Be a Mentor!</h2></div>",
        background="event/backgrounds/photo0_cBUZ8zp.jpg",
        is_public=True,
        position=40,
        event=past_event,
    )
    coach_content.coaches.add(coach)
    sponsor_content = EventPageContent.objects.create(
        name="partners", content="<h3>Sponsors</h3>", background="", is_public=True, position=50, event=past_event
    )
    sponsor_content.sponsors.add(sponsor)


@pytest.fixture
def past_event_menu(past_event):
    EventPageMenu.objects.create(url="#values", position=1, event=past_event, title="About")
    EventPageMenu.objects.create(url="#apply", position=10, event=past_event, title="Apply for a pass!")
    EventPageMenu.objects.create(url="#faq", position=10, event=past_event, title="FAQ")


@pytest.fixture
def blog_posts(db):
    return Story.objects.bulk_create(
        [
            Story(name="Post 1", content="Lorem ipsum dolor sit amet", is_story=False, post_url="post-1-url"),
            Story(name="Post 2", content="Lorem ipsum dolor sit amet", is_story=False, post_url="post-2-url"),
            Story(name="Post 3", content="Lorem ipsum dolor sit amet", is_story=False, post_url="post-3-url"),
            Story(name="Post 4", content="Lorem ipsum dolor sit amet", is_story=False, post_url="post-4-url"),
            Story(name="Post 5", content="Lorem ipsum dolor sit amet", is_story=False, post_url="post-5-url"),
        ]
    )


@pytest.fixture
def global_partners(db):
    return GlobalPartner.objects.bulk_create(
        [
            GlobalPartner(
                company_name="Django Software Foundation",
                contact_person="DSF Board",
                contact_email="dsfboard@djangoproject.com",
                sponsor_level_annual=5000,
                date_joined="2017-09-17",
                logo="django.logo",
                is_displayed=True,
                website_url="https://www.djangoproject.com",
                style="margin-top: 40px",
            ),
            GlobalPartner(
                company_name="TorchBox",
                contact_person="Jane Doe",
                contact_email="jane@torchbox.com",
                patreon_sponsor=True,
                patreon_level_per_month=250,
                sponsor_level_annual=2500,
                date_joined="2018-09-19",
                logo="torchbox.logo",
                is_displayed=True,
                website_url="https://torchbox.com",
                style="margin-top: 50px",
            ),
            GlobalPartner(
                company_name="Platform.sh",
                contact_person="John Doe",
                contact_email="john.doe@platform.sh",
                sponsor_level_annual=10000,
                date_joined="2023-02-02",
                logo="platform.jpg",
                is_displayed=True,
                website_url="https://platform.sh",
                style="margin-top: 25px",
            ),
            GlobalPartner(
                company_name="SixFeetUp",
                contact_person="Jane Doe",
                contact_email="jane.doe@sixfeetup.com",
                sponsor_level_annual=1000,
                date_joined="2021-11-15",
                logo="sixfeetup.png",
                is_displayed=True,
                website_url="https://sixfeetup.com",
                style="margin-top: 50px",
            ),
            GlobalPartner(
                company_name="Nexmo",
                contact_person="John Doe",
                contact_email="johndoe@vonage.com",
                sponsor_level_annual=500,
                date_joined="2018-11-15",
                logo="nexmo.png",
                is_displayed=False,
                website_url="https://nexmo.com",
                style="margin-top: 50px",
            ),
        ]
    )


@pytest.fixture
def old_event(organizer_peter):
    event = Event.objects.create(
        email="bonn@djangogirls.org",
        city="Bonn",
        name="Django Girls Bonn",
        country="the Neverlands",
        is_on_homepage=True,
        main_organizer=organizer_peter,
        date="2023-01-01",
        page_url="bonn",
        is_page_live=True,
    )
    event.team.add(organizer_peter)
    return event
