from django.test import TestCase

from core.deploy_event import (
    copy_content_from_previous_event,
    copy_menu_from_previous_event,
)
from core.models import Coach, Event, Sponsor


class CopyEventTest(TestCase):
    fixtures = ['core_views_testdata.json', 'groups_testdata.json']

    def test_copy_event(self):
        pass

    def test_copy_content_from_previous_event(self):
        previous_event = Event.objects.get(pk=1)
        new_event = Event.objects.create()
        self.assertEquals(new_event.content.count(), 0)
        copy_content_from_previous_event(previous_event, new_event)
        self.assertEquals(new_event.content.count(), 7)

        coaches = Coach.objects.filter(eventpagecontent__event=new_event)
        sponsors = Sponsor.objects.filter(eventpagecontent__event=new_event)
        self.assertEquals(coaches.count(), 1)
        self.assertEquals(sponsors.count(), 1)

    def test_copy_menu_from_previous_event(self):
        previous_event = Event.objects.get(pk=1)
        new_event = Event.objects.create()
        self.assertEquals(new_event.menu.count(), 0)
        copy_menu_from_previous_event(previous_event, new_event)
        self.assertEquals(new_event.menu.count(), 5)
