import pytest
from django.urls import reverse

from organize.constants import ACCEPTED, IN_REVIEW, ON_HOLD

IDENTITY = ("London", "Smith", "test@example.com")


@pytest.fixture
def change_url(base_application):
    return reverse("admin:organize_eventapplication_change", args=[base_application.pk])


def test_changelist_hides_identity_of_new_applications(admin_client, base_application):
    response = admin_client.get(reverse("admin:organize_eventapplication_changelist"))

    content = response.content.decode()
    assert f"Application #{base_application.pk}" in content
    for value in IDENTITY:
        assert value not in content


@pytest.mark.parametrize("status", [ON_HOLD, ACCEPTED])
def test_changelist_shows_identity_after_review(admin_client, base_application, status):
    base_application.change_status_to(status)

    response = admin_client.get(reverse("admin:organize_eventapplication_changelist"))

    content = response.content.decode()
    for value in IDENTITY:
        assert value in content


def test_change_page_hides_identity_of_anonymous_application(admin_client, application_with_coorganizer, change_url):
    response = admin_client.get(change_url)

    content = response.content.decode()
    assert response.status_code == 200
    assert "Reveal details" in content
    for value in (*IDENTITY, "anna@example.com"):
        assert value not in content


def test_reveal_shows_identity_to_this_reviewer(admin_client, application_with_coorganizer, change_url):
    reveal_url = reverse("admin:organize_eventapplication_reveal", args=[application_with_coorganizer.pk])

    response = admin_client.get(reveal_url)
    assert response.url == change_url

    content = admin_client.get(change_url).content.decode()
    assert "Reveal details" not in content
    for value in (*IDENTITY, "anna@example.com"):
        assert value in content


def test_saving_anonymous_application_keeps_hidden_fields(admin_client, base_application, change_url):
    response = admin_client.post(change_url, {"date": "2080-10-10", "comment": "Looks good", "_save": "Save"})

    assert response.status_code == 302
    base_application.refresh_from_db()
    assert base_application.comment == "Looks good"
    assert base_application.city == "London"
    assert base_application.main_organizer_email == "test@example.com"


def test_search_does_not_reveal_anonymous_applications(admin_client, base_application):
    url = reverse("admin:organize_eventapplication_changelist")

    assert admin_client.get(url, {"q": "London"}).context["cl"].result_count == 0

    base_application.change_status_to(ON_HOLD)
    assert admin_client.get(url, {"q": "London"}).context["cl"].result_count == 1


def test_triage_message_stays_anonymous(admin_client, base_application):
    url = reverse("admin:organize_eventapplication_change_application_status", args=[base_application.pk, IN_REVIEW])

    response = admin_client.get(url, follow=True)

    message = str(next(iter(response.context["messages"])))
    assert message == f"Application #{base_application.pk} has been moved to In review"
