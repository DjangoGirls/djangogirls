from django.test import TestCase

from core.models import Event, EventPage


class TestEventModel(TestCase):
    fixtures = ['core_views_testdata.json']

    def test_delete(self):
        self.assertTrue(Event.objects.all(), 4)
        event = Event.objects.get(pk=1)
        event.delete()
        self.assertTrue(Event.objects.all(), 3)
        event = Event.all_objects.get(pk=1)
        self.assertTrue(event.is_deleted)


class TestEventPageModel(TestCase):
    fixtures = ['core_views_testdata.json']

    def test_delete(self):
        self.assertTrue(EventPage.objects.all(), 4)
        event_page = EventPage.objects.get(pk=1)
        event_page.delete()
        self.assertTrue(EventPage.objects.all(), 3)
        event_page = EventPage.all_objects.get(pk=1)
        self.assertTrue(event_page.is_deleted)
