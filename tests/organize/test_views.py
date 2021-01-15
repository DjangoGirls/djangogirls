from django.urls import reverse
from formtools.wizard.views import NamedUrlSessionWizardView

from organize.forms import (
    PreviousEventForm, ApplicationForm, WorkshopForm,  WorkshopTypeForm, RemoteWorkshopForm, OrganizersFormSet)
from organize.models import EventApplication


def test_form_thank_you(client):
    # Access the thank you page
    resp = client.get(reverse('organize:form_thank_you'))
    assert resp.status_code == 200


def test_index(client):
    # Access the organize homepage
    resp = client.get(reverse('organize:index'))
    assert resp.status_code == 200


def test_commitment(client):
    # Access the commitment page
    resp = client.get(reverse('organize:commitment'))
    assert resp.status_code == 200


def test_prerequisites(client):
    # Access prerequisites page
    resp = client.get(reverse('organize:prerequisites'))
    assert resp.status_code == 200


def test_suspend(client):
    # Access suspend page
    resp = client.get(reverse('organize:suspend'))
    assert resp.status_code == 200


"""
def test_organize_form_wizard_remote_previous_organizer(client, previous_organizer_remote,
                                                        previous_application_more_than_6_months):
    # Test form submission for remote workshop with previous organizer
    for step, data_step in previous_organizer_remote:
        url = '/organize/form/' + step + '/'
        resp = client.get(url)
        assert resp.status_code == 200
        
        response = client.post(url, data_step)

        if step == len(previous_organizer_remote):
            assert response.status_code == 302
            assert response['Location'] == reverse('organize:form_thank_you')


def test_organize_form_wizard_remote_new_organizer(client, new_organizer_remote, no_previous_application):
    # Test form submission for remote workshop with new organizer
    for step, data_step in new_organizer_remote:
        url = '/organize/form/' + step + '/'
        response = client.post(url, data_step)
        if step == len(new_organizer_remote):
            assert response.status_code == 302
            assert response['Location'] == reverse('organize:form_thank_you')


def test_organize_form_wizard_in_person_previous_organizer(client, previous_organizer_in_person,
                                                           previous_event_in_more_than_6_months):
    # Test form submission for in-person workshop with previous organizer
    for step, data_step in previous_organizer_in_person:
        url = '/organize/form/' + step + '/'
        response = client.post(url, data_step)
        if step == len(previous_organizer_in_person):
            assert response.status_code == 302
            assert response['Location'] == reverse('organize:form_thank_you')


def test_organize_form_wizard_in_person_new_organizer(client, new_organizer_in_person, no_previous_event):
    # Test form submission for in-person with new organizer
    for step, data_step in new_organizer_in_person:
        url = '/organize/form/' + step + '/'
        response = client.post(url, data_step)
        if step == len(new_organizer_in_person):
            assert response.status_code == 302
            assert response['Location'] == reverse('organize:form_thank_you')


def test_organize_form_wizard_applications_too_close(client, previous_organizer_remote,
                                                     previous_application_less_than_6_months):
    # Test form submission with applications less than 6 months apart
    for step, data_step in previous_organizer_remote:
        url = '/organize/form/' + step + '/'
        response = client.post(url, data_step)
        if step == len(previous_organizer_remote):
            assert response.status_code == 302
            assert response['Location'] == reverse('organize:prerequisites')
            assert response['form.errors'] == 'You cannot apply to organize an event when you ' \
                                              'have another open application.'


def test_organize_form_wizards_workshops_too_close(client, previous_organizer_in_person,
                                                   previous_event_in_6_months):
    # Test form submission with workshops less than 6 months apart
    for step, data_step in previous_organizer_in_person:
        url = '/organize/form/' + step + '/'
        response = client.post(url, data_step)
        if step == len(previous_organizer_in_person):
            assert response.status_code == 302
            assert response['Location'] == reverse('organize:form_thank_you')
"""
