from datetime import timedelta

from django.contrib.auth.models import Group
from django.test import TestCase
from django.utils import timezone
from django_date_extensions.fields import ApproximateDate

from coach.models import Coach, DEFAULT_COACH_PHOTO
from core.models import Event, User


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

    def test_is_upcoming(self):
        now = timezone.now()
        now_event = Event(date=ApproximateDate(now.year, now.month, now.day))
        yesterday = now - timedelta(days=1)
        yesterday_event = Event(date=ApproximateDate(
            yesterday.year, yesterday.month, yesterday.day
        ))
        tomorrow = now + timedelta(days=1)
        tomorrow_event = Event(date=ApproximateDate(
            tomorrow.year, tomorrow.month, tomorrow.day
        ))
        assert now_event.is_upcoming()
        assert not yesterday_event.is_upcoming()
        assert tomorrow_event.is_upcoming()


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
