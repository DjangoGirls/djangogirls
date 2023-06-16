from datetime import datetime

import pytest
from django.contrib.auth.models import Group, Permission

from core.models import Event, User
from core.tumblr_client import RemoteStory
from globalpartners.models import GlobalPartner
from pictures.models import StockPicture
from sponsor.models import Donor
from tests.mocks import *  # noqa


@pytest.fixture(autouse=True)
def default_mocks(slack_mock):
    """
    Add mocks that should be accessible for all tests in this function signature.
    """


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture()
def user(db, django_user_model, django_username_field):
    """This is a copy from pytest-django prepared for usage with e-mail instead
    of username.
    """
    UserModel = django_user_model
    username_field = django_username_field

    try:
        user = UserModel._default_manager.get(**{username_field: "user@example.com"})
    except UserModel.DoesNotExist:
        extra_fields = {}
        user = UserModel._default_manager.create_user("user@example.com", "password", **extra_fields)
    return user


@pytest.fixture()
def admin_user(db, django_user_model, django_username_field):
    """This is a copy from pytest-django prepared for usage with e-mail instead
    of username.
    """
    UserModel = django_user_model
    username_field = django_username_field

    try:
        user = UserModel._default_manager.get(**{username_field: "admin@example.com"})
    except UserModel.DoesNotExist:
        extra_fields = {}
        user = UserModel._default_manager.create_superuser("admin@example.com", "password", **extra_fields)
    return user


@pytest.fixture()
def admin_client(db, admin_user):
    """A Django test client logged in as an admin user."""
    from django.test.client import Client

    client = Client()
    client.force_login(admin_user)
    return client


@pytest.fixture()
def user_client(db, user):
    """A Django test client logged in as an user."""
    from django.test.client import Client

    client = Client()
    client.force_login(user)
    return client


@pytest.fixture()
def organizers_group():
    add_event_permission = Permission.objects.get(codename="add_event")
    change_event_permission = Permission.objects.get(codename="change_event")
    group = Group.objects.create(name="Organizers")
    group.permissions.set([add_event_permission, change_event_permission])
    return group


@pytest.fixture()
def superuser():
    return User.objects.create(
        first_name="Super",
        last_name="Girl",
        email="super-girl@example.com",
        is_active=True,
        is_superuser=True,
        is_staff=True,
    )


@pytest.fixture()
def organizer_peter(organizers_group):
    user = User.objects.create(
        first_name="Peter",
        last_name="Pan",
        email="peter-pan@example.com",
        password="",
        is_active=True,
        is_superuser=False,
        is_staff=True,
    )
    user.groups.add(organizers_group)
    return user


@pytest.fixture()
def organizer_julia(organizers_group):
    user = User.objects.create(
        first_name="Julia",
        last_name="Ailuj",
        email="julia-ailuj@example.com",
        password="",
        is_active=True,
        is_superuser=False,
        is_staff=True,
    )
    user.groups.add(organizers_group)
    return user


@pytest.fixture()
def future_event(organizer_peter):
    event = Event.objects.create(
        email="bonn@djangogirls.org",
        city="Bonn",
        name="Django Girls Bonn",
        country="the Neverlands",
        is_on_homepage=True,
        main_organizer=organizer_peter,
        date="2080-01-01",
        page_url="bonn",
        is_page_live=True,
    )
    event.team.add(organizer_peter)
    return event


@pytest.fixture()
def past_event(organizer_peter):
    event = Event.objects.create(
        email="rome@djangogirls.org",
        city="Rome",
        name="Django Girls Rome",
        country="Italy",
        latlng="41.8933203, 12.4829321",
        is_on_homepage=True,
        main_organizer=organizer_peter,
        date="2013-10-12",
        page_url="rome",
        is_page_live=True,
    )
    event.team.add(organizer_peter)
    return event


@pytest.fixture()
def hidden_event(superuser):
    event = Event.objects.create(
        email="rome@djangogirls.org",
        city="Rome",
        name="Django Girls Rome",
        country="Italy",
        is_on_homepage=False,
        main_organizer=superuser,
        date="2080-09-02",
        page_url="rome",
        is_page_live=False,
    )
    event.team.add(superuser)
    return event


@pytest.fixture()
def diff_url_event(superuser):
    event = Event.objects.create(
        email="foo@djangogirls.org",
        city="Foo",
        name="Django Girls Foo",
        country="Italy",
        is_on_homepage=False,
        main_organizer=superuser,
        date="2080-09-02",
        page_url="bar",
        is_page_live=False,
    )
    event.team.add(superuser)
    return event


@pytest.fixture()
def no_date_event(superuser):
    event = Event.objects.create(
        email="venice@djangogirls.org",
        city="Venice",
        name="Django Girls Venice",
        country="Italy",
        is_on_homepage=False,
        main_organizer=superuser,
        page_url="venice",
        is_page_live=False,
    )
    event.team.add(superuser)
    return event


@pytest.fixture()
def events(future_event, past_event, hidden_event, no_date_event):
    return [future_event, past_event, hidden_event, no_date_event]


@pytest.fixture()
def stock_pictures():
    StockPicture.objects.bulk_create(
        [
            StockPicture(
                photo="stock_pictures/city_one.jpg",
                photo_credit="Someone",
                photo_link="https://djangogirls.org",
                kind=StockPicture.COVER,
            ),
            StockPicture(
                photo="stock_pictures/city_two.jpg",
                photo_credit="Someone Else",
                photo_link="https://djangogirls.org",
                kind=StockPicture.COVER,
            ),
        ]
    )


@pytest.fixture()
def visible_donors():
    donors = Donor.objects.bulk_create(
        [
            Donor(name="Ola", amount=50, visible=True),
            Donor(name="Aisha", amount=50, visible=True),
            Donor(name="Claire", amount=20, visible=True),
            Donor(name="Rachel", amount=100, visible=True),
        ]
    )
    return donors


@pytest.fixture()
def hidden_donors():
    hidden_donors = Donor.objects.bulk_create(
        [
            Donor(name="Gift", amount=20, visible=False),
            Donor(name="Anna", amount=10, visible=False),
            Donor(name="Matthew", amount=50, visible=False),
            Donor(name="Tanaka", amount=100, visible=False),
        ]
    )
    return hidden_donors


@pytest.fixture()
def remote_story():
    return RemoteStory(
        url="tumblr.com/stories/1",
        content_parts=[
            {"text": "This is a story text", "type": "text"},
            {"text": "This is another story text", "type": "text"},
            {
                "media": [{"url": "/media-small"}, {"url": "/media-large"}],
                "type": "image",
            },
        ],
        created=datetime.utcnow(),
    )


@pytest.fixture
def globalpartner(db):
    return GlobalPartner.objects.create(
        company_name="Django Software Foundation",
        contact_person="Jane Doe",
        contact_email="jane@djangoproject.com",
        logo="django.png",
        is_displayed=True,
        sponsor_level_annual=5000,
    )


@pytest.fixture
def globalpartner2(db):
    return GlobalPartner.objects.create(
        company_name="Caktus Group",
        contact_person="Jane Doe",
        contact_email="jane@caktus.com",
        logo="caktus.png",
        is_displayed=True,
        sponsor_level_annual=2500,
    )
