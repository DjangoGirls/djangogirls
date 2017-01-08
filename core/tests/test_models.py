from django.contrib.auth.models import Group
from django.test import TestCase

from core.models import DEFAULT_COACH_PHOTO, Coach, Event, User


class TestEventModel(TestCase):
    fixtures = ['core_views_testdata.json']

    def test_delete(self):
        self.assertTrue(Event.objects.all(), 4)
        event = Event.objects.get(pk=1)
        event.delete()
        self.assertTrue(Event.objects.all(), 3)
        event = Event.all_objects.get(pk=1)
        self.assertTrue(event.is_deleted)

    def test_has_stats(self):
        event = Event()
        self.assertFalse(event.has_stats)

        event = Event(applicants_count=10)
        self.assertFalse(event.has_stats)

        event = Event(attendees_count=20)
        self.assertFalse(event.has_stats)

        event = Event(attendees_count=20, applicants_count=40)
        self.assertTrue(event.has_stats)

    def test_add_default_content(self):
        event = Event.objects.get(pk=1)
        event.content.all().delete()
        self.assertEquals(event.content.count(), 0)
        event.add_default_content()
        self.assertEquals(event.content.count(), 7)

    def test_add_default_menu(self):
        event = Event.objects.get(pk=1)
        event.menu.all().delete()
        self.assertEquals(event.menu.count(), 0)
        event.add_default_menu()
        self.assertEquals(event.menu.count(), 5)

    def test_invite_organizer_to_team(self):
        event = Event.objects.get(pk=1)
        self.assertEquals(event.team.count(), 2)
        user = User.objects.create(
            first_name="Alice",
            last_name="Smith",
            is_staff=True,
            is_active=True
        )
        event.invite_organizer_to_team(user, is_new_user=True, password="pass")
        self.assertEquals(event.team.count(), 3)


class TestCoachModel(TestCase):
    def test_delete(self):
        self.assertEquals(Coach.objects.count(), 0)
        coach = Coach.objects.create(name="Test Test", twitter_handle="@test")
        self.assertEquals(Coach.objects.count(), 1)
        self.assertEqual(coach.photo_url, DEFAULT_COACH_PHOTO)


class UserModel(TestCase):
    fixtures = ['core_views_testdata.json']

    def test_add_to_organizers_group(self):
        user = User.objects.get(pk=1)
        self.assertEquals(user.groups.count(), 0)
        user.add_to_organizers_group()
        # we don't have Group "Oragnizers", so no group is added
        self.assertEquals(user.groups.count(), 0)

        Group.objects.create(name="Organizers")
        user.add_to_organizers_group()
        self.assertEquals(user.groups.count(), 1)
