from django.test import TestCase

from core.models import DEFAULT_COACH_PHOTO, Coach, Event, EventPage


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


class TestCoachModel(TestCase):
    def test_delete(self):
        self.assertEquals(Coach.objects.count(), 0)
        coach = Coach.objects.create(name="Test Test", twitter_handle="@test")
        self.assertEquals(Coach.objects.count(), 1)
        self.assertEqual(coach.photo_url, DEFAULT_COACH_PHOTO)
