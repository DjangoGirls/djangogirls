import pytest
from django.contrib.admin.sites import AdminSite
from django.urls import reverse

from coach.admin import CoachAdmin
from coach.models import Coach
from core.models import EventPageContent


@pytest.fixture
def coach_admin():
    return CoachAdmin(Coach, AdminSite())


def test_get_queryset_for_organizer_no_duplicates(client, organizer_peter, future_event):
    """A coach linked to multiple EventPageContent blocks should appear only once
    in the queryset, preventing MultipleObjectsReturned when the admin calls get()."""
    coach = Coach.objects.create(name="Anna Smith")

    content1 = EventPageContent.objects.create(event=future_event, name="coaches", content="a", position=1)
    content2 = EventPageContent.objects.create(event=future_event, name="mentors", content="b", position=2)
    content1.coaches.add(coach)
    content2.coaches.add(coach)

    client.force_login(organizer_peter)
    admin_instance = CoachAdmin(Coach, AdminSite())
    request = client.get(reverse("admin:coach_coach_changelist")).wsgi_request
    request.user = organizer_peter

    qs = admin_instance.get_queryset(request)
    assert qs.filter(pk=coach.pk).count() == 1


def test_get_queryset_for_superuser_returns_all(admin_client, admin_user):
    """Superuser should see all coaches."""
    Coach.objects.create(name="Coach A")
    Coach.objects.create(name="Coach B")

    admin_instance = CoachAdmin(Coach, AdminSite())
    request = admin_client.get(reverse("admin:coach_coach_changelist")).wsgi_request
    request.user = admin_user

    qs = admin_instance.get_queryset(request)
    assert qs.count() == 2
