from datetime import timedelta

from django.contrib.auth.models import Group
from django.utils import timezone
from django_date_extensions.fields import ApproximateDate

from core.models import Event, User


def test_delete(events):
    assert Event.objects.count() == 4
    event = events[0]
    event.delete()
    assert Event.objects.count() == 3
    event = Event.all_objects.get(pk=event.pk)
    assert event.is_deleted is True


def test_has_stats():
    event = Event()
    assert event.has_stats is False

    event = Event(applicants_count=10)
    assert event.has_stats is False

    event = Event(attendees_count=20)
    assert event.has_stats is False

    event = Event(attendees_count=20, applicants_count=40)
    assert event.has_stats is True


def test_add_default_content(future_event):
    future_event.content.all().delete()
    assert future_event.content.count() == 0
    future_event.add_default_content()
    assert future_event.content.count() == 7


def test_add_default_menu(future_event):
    future_event.menu.all().delete()
    assert future_event.menu.count() == 0
    future_event.add_default_menu()
    assert future_event.menu.count() == 5


def test_invite_organizer_to_team(future_event):
    assert future_event.team.count() == 1
    user = User.objects.create(first_name="Alice", last_name="Smith", is_staff=True, is_active=True)
    future_event.invite_organizer_to_team(user, is_new_user=True, password="pass")
    assert future_event.team.count() == 2


def test_is_upcoming():
    now = timezone.now()
    now_event = Event(date=ApproximateDate(now.year, now.month, now.day))
    yesterday = now - timedelta(days=1)
    yesterday_event = Event(date=ApproximateDate(yesterday.year, yesterday.month, yesterday.day))
    tomorrow = now + timedelta(days=1)
    tomorrow_event = Event(date=ApproximateDate(tomorrow.year, tomorrow.month, tomorrow.day))
    assert now_event.is_upcoming()
    assert not yesterday_event.is_upcoming()
    assert tomorrow_event.is_upcoming()


def test_add_to_organizers_group(user):
    assert not Group.objects.filter(name="Organizers").exists()
    assert user.groups.count() == 0
    user.add_to_organizers_group()
    # we don't have Group "Organizers", so no group is added
    assert user.groups.count() == 0

    Group.objects.create(name="Organizers")
    user.add_to_organizers_group()
    assert user.groups.count() == 1


def test_has_organizer_no_organizer(user, future_event):
    future_event.main_organizer = None
    future_event.team.clear()

    assert not future_event.has_organizer(user)


def test_has_organizer_in_team(user, future_event):
    future_event.main_organizer = None
    future_event.team.add(user)

    assert future_event.has_organizer(user)


def test_has_organizer_main_organizer(user, future_event):
    future_event.main_organizer = user
    future_event.team.clear()

    assert future_event.has_organizer(user)


def test_event_lnglat(future_event):
    assert future_event.lnglat == ""

    future_event.latlng = "39.4747112, -0.3798073"
    assert future_event.lnglat == "-0.3798073, 39.4747112"

    future_event.latlng = "sddasdasda"
    assert future_event.lnglat == ""
