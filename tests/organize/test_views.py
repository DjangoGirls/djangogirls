import pytest
from django.template.loader import render_to_string
from django.urls import reverse


def test_form_thank_you(client):
    # Access the thank you page
    resp = client.get(reverse("organize:form_thank_you"))
    assert resp.status_code == 200


def test_index(client):
    # Access the organize homepage
    resp = client.get(reverse("organize:index"))
    assert resp.status_code == 200


def test_commitment(client):
    # Access the commitment page
    resp = client.get(reverse("organize:commitment"))
    assert resp.status_code == 200


def test_prerequisites(client):
    # Access prerequisites page
    resp = client.get(reverse("organize:prerequisites"))
    assert resp.status_code == 200


def test_suspend(client):
    # Access suspend page
    resp = client.get(reverse("organize:suspend"))
    assert resp.status_code == 200


def organize_view(client, workshop_data, previous_application, previous_event):
    for step, data_step in workshop_data:
        url = reverse("organize:form_step", kwargs={"step": step})
        resp = client.get(url)
        assert resp.status_code == 200
        response = client.post(url, data_step)
        assert response.content != render_to_string("organize/form/thank_you.html")
        if step == len(workshop_data):
            # Final step
            assert response.content == render_to_string("organize/form/thank_you.html")
            assert response.status_code == 302
            assert response["Location"] == reverse("organize:form_thank_you")


@pytest.mark.django_db(transaction=True)
def test_organize_form_wizard_remote_previous_organizer(
    client, previous_organizer_remote, previous_event_more_than_6_months, previous_application=None
):
    # Test form submission for remote workshop with previous organizer
    organize_view(client, previous_organizer_remote, previous_event_more_than_6_months, previous_application)


def test_organize_form_wizard_remote_new_organizer(
    client, new_organizer_remote, previous_application=None, previous_event=None
):
    # Test form submission for remote workshop with new organizer
    organize_view(client, new_organizer_remote, previous_application, previous_event)


def test_organize_form_wizard_in_person_previous_organizer(
    client, previous_organizer_in_person, previous_application_more_than_6_months, previous_event_more_than_6_months
):
    # Test form submission for in-person workshop with previous organizer
    organize_view(
        client, previous_organizer_in_person, previous_application_more_than_6_months, previous_event_more_than_6_months
    )


def test_organize_form_wizard_in_person_new_organizer(
    client, new_organizer_in_person, previous_application=None, previous_event=None
):
    # Test form submission for in-person with new organizer
    organize_view(client, new_organizer_in_person, previous_application, previous_event)


def test_organize_form_wizard_applications_too_close(
    client, previous_organizer_remote, previous_application_less_than_6_months
):
    # Test form submission with applications less than 6 months apart
    for step, data_step in previous_organizer_remote:
        url = reverse("organize:form_step", kwargs={"step": step})
        response = client.post(url, data_step)
        if step == len(previous_organizer_remote):
            assert response.status_code == 302
            assert response["Location"] == reverse("organize:prerequisites")
            assert (
                response["form.errors"] == "You cannot apply to organize another event when you "
                "already have another open event application."
            )


def test_organize_form_wizard_workshops_too_close(client, previous_organizer_in_person, future_event):
    # Test form submission with workshops less than 6 months apart
    for step, data_step in previous_organizer_in_person:
        url = reverse("organize:form_step", kwargs={"step": step})
        response = client.post(url, data_step)
        if step == len(previous_organizer_in_person):
            assert response.status_code == 302
            assert response["Location"] == reverse("organize:prerequisites")
            assert (
                response["form.errors"] == "Your workshops should be at least 6 months apart. "
                "Please read our Organizer Manual."
            )
