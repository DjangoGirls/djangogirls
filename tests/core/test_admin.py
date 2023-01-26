from datetime import datetime
from unittest import mock

from django.urls import reverse

from core.models import Event


def test_get_queryset_for_superuser(admin_client, events):
    resp = admin_client.get(reverse("admin:core_event_changelist"))
    assert len(resp.context["results"]) == 4


def test_get_queryset_for_organizer(client, organizer_peter, future_event, past_event):
    client.force_login(organizer_peter)
    resp = client.get(reverse("admin:core_event_changelist"))
    assert len(resp.context["results"]) == 2
    # flattens the list of lists
    # FIXME
    results = "".join(sum(resp.context["results"], []))
    assert all([x.name in results for x in [future_event, past_event]])


def test_manage_organizers_view_for_superuser(admin_client, events):
    resp = admin_client.get(reverse("admin:core_event_manage_organizers"))

    # Only upcoming events are listed
    expected_events = Event.objects.filter(date__gte=datetime.now().strftime("%Y-%m-%d")).order_by("name")
    assert len(resp.context["all_events"]) == expected_events.count()
    assert all([x.is_upcoming() for x in resp.context["all_events"]])

    # First event is selected automatically
    assert resp.context["event"] == expected_events[0]


def test_manage_organizers_view_for_organizers(client, organizer_peter, events):
    expected_events = Event.objects.filter(date__gte=datetime.now().strftime("%Y-%m-%d"), team=organizer_peter)
    client.force_login(organizer_peter)
    resp = client.get(reverse("admin:core_event_manage_organizers"))
    assert len(resp.context["all_events"]) == expected_events.count()
    assert all([x.is_upcoming() for x in resp.context["all_events"]])


@mock.patch("core.models.User.invite_to_slack")
def test_adding_organizer_as_superuser(invite_to_slack, admin_client, future_event, hidden_event, django_user_model):
    add_organizers_url = reverse("admin:core_event_add_organizers")
    total_count = django_user_model.objects.filter(is_staff=True).count()
    team_count = future_event.team.count()
    data = {"event": future_event.pk, "name": "New organizer", "email": "new-superuser@organizer.com"}
    resp = admin_client.post(reverse("admin:core_event_add_organizers"), data)
    assert resp.status_code == 302
    assert django_user_model.objects.filter(is_staff=True).count() == (total_count + 1)
    assert future_event.team.count() == (team_count + 1)

    # Adding already existing organizer
    team_count = hidden_event.team.count()
    data = {"event": hidden_event.pk, "name": "New organizer", "email": "new-superuser@organizer.com"}
    resp = admin_client.post(reverse("admin:core_event_add_organizers"), data)
    assert resp.status_code == 302
    assert django_user_model.objects.filter(is_staff=True).count() == (total_count + 1)
    assert hidden_event.team.count() == (team_count + 1)


@mock.patch("core.models.User.invite_to_slack")
def test_organizer_can_only_add_to_their_event(invite_to_slack, client, organizer_peter, future_event, hidden_event):
    add_organizers_url = reverse("admin:core_event_add_organizers")
    client.force_login(organizer_peter)
    data = {"event": hidden_event.pk, "name": "New organizer", "email": "new@organizer.com"}
    # Mock call to slack
    resp = client.post(add_organizers_url, data)
    assert resp.status_code == 200
    assert len(resp.context["form"].errors) == 1

    data = {"event": future_event.pk, "name": "New organizer", "email": "new@organizer.com"}
    resp = client.post(add_organizers_url, data)
    assert resp.status_code == 302


def test_remove_organizer_as_superuser(admin_client, organizer_julia, organizer_peter, future_event):
    future_event.team.add(organizer_julia)
    future_event.save()
    assert future_event.team.count() == 2

    data = {
        "event_id": future_event.pk,
        "remove": organizer_peter.pk,
    }
    resp = admin_client.get(reverse("admin:core_event_manage_organizers"), data)
    assert resp.status_code == 302
    assert future_event.team.count() == 1


def test_organizers_can_only_remove_from_their_events(
    client, organizer_peter, superuser, organizer_julia, hidden_event, future_event
):
    future_event.team.add(organizer_julia)
    manage_organizers_url = reverse("admin:core_event_manage_organizers")
    client.force_login(organizer_peter)
    data = {"event_id": hidden_event.pk, "remove": superuser.pk}

    assert hidden_event.team.count() == 1
    resp = client.get(manage_organizers_url, data)
    assert resp.status_code == 200
    assert hidden_event.team.count() == 1

    data = {"event_id": future_event.pk, "remove": organizer_julia.pk}

    assert future_event.team.count() == 2
    resp = client.get(manage_organizers_url, data)
    assert resp.status_code == 302
    assert future_event.team.count() == 1


def test_organizers_cannot_remove_themselves(client, organizer_peter, future_event, organizer_julia):
    future_event.team.add(organizer_julia)
    manage_organizers_url = reverse("admin:core_event_manage_organizers")
    client.force_login(organizer_peter)
    data = {
        "event_id": future_event.pk,
        "remove": organizer_peter.pk,
    }
    assert future_event.team.count() == 2
    resp = client.get(manage_organizers_url, data)
    assert resp.status_code == 200
    assert future_event.team.count() == 2

    data = {
        "event_id": future_event.pk,
        "remove": organizer_julia.pk,
    }
    assert future_event.team.count() == 2
    resp = client.get(manage_organizers_url, data)
    assert resp.status_code == 302
    assert future_event.team.count() == 1


def test_clone_events_admin(admin_client, future_event):
    to_be_cloned = Event.objects.values_list("pk", flat=True)
    data = {"action": "clone_action", "_selected_action": to_be_cloned}

    change_url = reverse("admin:core_event_changelist")
    response = admin_client.post(change_url, data, follow=True)
    assert response.status_code == 200
    assert Event.objects.filter(name__icontains="clone").count() == 1


def test_freeze_events_action(admin_client, future_event):
    to_be_frozen = Event.objects.values_list("pk", flat=True)
    data = {"action": "freeze_action", "_selected_action": to_be_frozen}

    change_url = reverse("admin:core_event_changelist")
    response = admin_client.post(change_url, data, follow=True)
    assert response.status_code == 200
    assert Event.objects.filter(is_frozen=True).count() == 1
    assert Event.objects.filter(is_on_homepage=False).count() == 1


def test_unfreeze_events_action(admin_client, future_event):
    to_be_unfrozen = Event.objects.values_list("pk", flat=True)
    data = {"action": "unfreeze_action", "_selected_action": to_be_unfrozen}

    change_url = reverse("admin:core_event_changelist")
    response = admin_client.post(change_url, data, follow=True)
    assert response.status_code == 200
    assert Event.objects.filter(is_frozen=False).count() == 1
    assert Event.objects.filter(is_on_homepage=True).count() == 1
