from datetime import date

from coach.models import Coach
from core.deploy_event import copy_content_from_previous_event, copy_event, copy_menu_from_previous_event
from core.models import Event
from sponsor.models import Sponsor


def test_copy_content_from_previous_event(past_event_page_content, past_event):
    new_event = Event.objects.create()
    assert new_event.content.count() == 0
    copy_content_from_previous_event(past_event, new_event)
    assert new_event.content.count() == past_event.content.count()

    # coaches and sponsors shouldn't carry over
    old_coaches = Coach.objects.filter(eventpagecontent__event=past_event)
    old_sponsors = Sponsor.objects.filter(eventpagecontent__event=past_event)
    assert old_coaches.count() > 0
    assert old_sponsors.count() > 0
    coaches = Coach.objects.filter(eventpagecontent__event=new_event)
    sponsors = Sponsor.objects.filter(eventpagecontent__event=new_event)
    assert coaches.count() == 0
    assert sponsors.count() == 0


def test_copy_menu_from_previous_event(past_event, past_event_menu):
    new_event = Event.objects.create()
    assert new_event.menu.count() == 0
    assert past_event.menu.count() > 0
    copy_menu_from_previous_event(past_event, new_event)
    assert new_event.menu.count() == past_event.menu.count()


def test_copy_event(past_event):
    previous_name = past_event.name
    previous_event_id = past_event.pk
    new_date = date(2021, 10, 20)

    new_event = copy_event(past_event, new_date)

    # we need to refetch the event as we changed id of the object
    # inside copy_event method
    past_event = Event.objects.get(pk=previous_event_id)

    assert past_event.name == f"{previous_name} #1"
    assert new_event.name == f"{previous_name} #2"
    assert past_event.date != new_event.date

    assert past_event.city == new_event.city
    assert past_event.country == new_event.country
    assert past_event.latlng == new_event.latlng
    assert past_event.main_organizer == new_event.main_organizer
