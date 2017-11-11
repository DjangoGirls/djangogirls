from datetime import date
from django.test import TestCase

from core.deploy_event import (
    copy_content_from_previous_event,
    copy_event,
    copy_menu_from_previous_event,
)
from coach.models import Coach
from core.models import Event
from sponsor.models import Sponsor


class CopyEventTest(TestCase):
    fixtures = ['core_views_testdata.json', 'groups_testdata.json']

    def test_copy_content_from_previous_event(self):
        previous_event = Event.objects.get(pk=1)
        new_event = Event.objects.create()
        self.assertEquals(new_event.content.count(), 0)
        copy_content_from_previous_event(previous_event, new_event)
        self.assertEquals(new_event.content.count(), 7)

        # coaches and sponsors shouldn't carry over
        coaches = Coach.objects.filter(eventpagecontent__event=new_event)
        sponsors = Sponsor.objects.filter(eventpagecontent__event=new_event)
        self.assertEquals(coaches.count(), 0)
        self.assertEquals(sponsors.count(), 0)

    def test_copy_menu_from_previous_event(self):
        previous_event = Event.objects.get(pk=1)
        new_event = Event.objects.create()
        self.assertEquals(new_event.menu.count(), 0)
        copy_menu_from_previous_event(previous_event, new_event)
        self.assertEquals(new_event.menu.count(), 5)

    def test_copy_event(self):
        previous_event = Event.objects.get(pk=1)
        previous_name = previous_event.name
        new_date = date(2020, 10, 20)

        new_event = copy_event(previous_event, new_date)

        # we need to refetch the event as we changed id of the object
        # inside copy_event method
        previous_event = Event.objects.get(pk=1)

        self.assertEquals(previous_event.name, "{} #1".format(previous_name))
        self.assertEquals(new_event.name, "{} #2".format(previous_name))
        self.assertTrue(previous_event.date != new_event.date)

        self.assertEquals(previous_event.city, new_event.city)
        self.assertEquals(previous_event.country, new_event.country)
        self.assertEquals(previous_event.latlng, new_event.latlng)
        self.assertEquals(previous_event.photo, new_event.photo)
        self.assertEquals(
            previous_event.main_organizer,
            new_event.main_organizer
        )