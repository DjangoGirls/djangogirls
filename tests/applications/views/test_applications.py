import random

import pytest
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from applications.models import Application, Score
from applications.views import application_list


def test_access_applications_view(client, user_client, admin_client, future_event):
    # as anonymous user
    applications_url = reverse(
        'applications:applications',
        kwargs={'city': future_event.page_url})
    resp = client.get(applications_url)
    assert resp.status_code == 302

    # as logged in user, but not orgarniser of given event
    resp = user_client.get(applications_url)
    assert resp.status_code == 404

    # as superuser
    resp = admin_client.get(applications_url)
    assert resp.status_code == 200

    # as organiser of given event
    client.force_login(future_event.main_organizer)
    resp = client.get(applications_url)
    assert resp.status_code == 200


def test_organiser_only_decorator_without_city(rf, user, future_event):
    request = rf.get('')
    request.user = user
    with pytest.raises(ValueError):
        application_list(request, city=None)


def test_organiser_menu_in_applications_list(admin_client, future_event):
    applications_url = reverse(
        'applications:applications',
        kwargs={'city': future_event.page_url})
    resp = admin_client.get(applications_url)
    messaging_url = reverse(
        'applications:communication',
        kwargs={'city': future_event.page_url})
    assert (
        '<a href="{}">Applications</a>'.format(applications_url)
        in str(resp.content.decode('utf-8')))
    assert (
        '<a href="{}">Messaging</a>'.format(messaging_url)
        in str(resp.content.decode('utf-8')))


def test_get_sorted_applications_list(
        application_submitted, application_accepted, application_rejected,
        application_waitlisted, admin_client, admin_user, future_event,
        superuser):
    applications_url = reverse(
        'applications:applications',
        kwargs={'city': future_event.page_url})

    # Add some scores:
    Score.objects.bulk_create([
        Score(application=application_submitted, user=admin_user, score=2.0),
        Score(application=application_submitted, user=superuser, score=4.0),
        Score(application=application_accepted, user=admin_user, score=3.0),
        Score(application=application_accepted, user=superuser, score=3.0),
        Score(application=application_rejected, user=admin_user, score=3.0),
        Score(application=application_rejected, user=superuser, score=4.0)
    ])

    # Order by average_score
    resp = admin_client.get('{}?order=average_score'.format(applications_url))
    assert resp.status_code == 200
    assert len(resp.context['applications']) == 4
    assert (
        resp.context['applications'] == [
            application_waitlisted, application_submitted, application_accepted,
            application_rejected
        ]
    )
    assert resp.context['order'] == 'average_score'

    # Order by -average_score
    resp = admin_client.get('{}?order=-average_score'.format(applications_url))
    assert resp.status_code == 200
    assert len(resp.context['applications']) == 4
    assert (
        resp.context['applications'] == [
            application_rejected, application_accepted, application_submitted,
            application_waitlisted
        ]
    )
    assert resp.context['order'] == '-average_score'


def get_filtered_applications_list(
    admin_client, future_event, application_submitted, application_accepted,
    application_rejected, application_waitlisted
):
    # No filter
    applications_url = reverse(
        'applications:applications',
        kwargs={'city': future_event.page_url})
    resp = admin_client.get(applications_url)
    assert len(resp.context['applications']) == 4

    # Filter by submitted
    resp.self.client.get('{}?state=submitted'.format(applications_url))
    assert len(resp.context['applications']) == 1
    assert resp.context['applications'] == [application_submitted]

    # Filter by accepted
    resp.self.client.get('{}?state=accepted'.format(applications_url))
    assert len(resp.context['applications']) == 1
    assert resp.context['applications'] == [application_accepted]

    # Filter by rejected
    resp.self.client.get('{}?state=rejected'.format(applications_url))
    assert len(resp.context['applications']) == 1
    assert resp.context['applications'] == [application_rejected]

    # Filter by wait listed
    resp.self.client.get('{}?state=waitlisted'.format(applications_url))
    assert len(resp.context['applications']) == 1
    assert resp.context['applications'] == [application_waitlisted]


def test_changing_application_status(
        admin_client, future_event, application_submitted):
    assert application_submitted.state == 'submitted'
    resp = admin_client.post(
        reverse('applications:change_state', args=[future_event.page_url]),
        {'state': 'accepted', 'application': application_submitted.id}
    )
    assert resp.status_code == 200
    application_submitted.refresh_from_db()
    assert application_submitted.state == 'accepted'


def test_yes_rsvp(client, future_event, application_accepted):
    assert application_accepted.rsvp_status == Application.RSVP_WAITING
    args = [future_event.page_url, application_accepted.get_rsvp_yes_code()]
    resp = client.get(
        reverse('applications:rsvp', args=args)
    )
    assert resp.status_code == 200
    application_accepted.refresh_from_db()
    assert application_accepted.rsvp_status == Application.RSVP_YES


def test_repeated_rsvp(client, future_event, application_accepted):
    application_accepted.rsvp_status = Application.RSVP_YES
    application_accepted.save()
    assert application_accepted.rsvp_status == Application.RSVP_YES
    args = [future_event.page_url, application_accepted.get_rsvp_no_code()]
    resp = client.get(
        reverse('applications:rsvp', args=args)
    )
    assert resp.status_code == 302
    application_accepted = Application.objects.get(id=application_accepted.id)
    assert application_accepted.rsvp_status == Application.RSVP_YES


def test_no_rsvp(client, future_event, application_accepted):
    application_accepted.rsvp_status = Application.RSVP_WAITING
    application_accepted.save()
    assert application_accepted.rsvp_status == Application.RSVP_WAITING
    args = [future_event.page_url, application_accepted.get_rsvp_no_code()]
    resp = client.get(
        reverse('applications:rsvp', args=args)
    )
    assert resp.status_code == 200
    application_accepted = Application.objects.get(id=application_accepted.id)
    assert application_accepted.rsvp_status == Application.RSVP_NO


def test_nonexistent_rsvp(client, future_event, application_accepted):
    assert application_accepted.rsvp_status == Application.RSVP_WAITING
    args = [future_event.page_url, 'sssss']
    resp = client.get(
        reverse('applications:rsvp', args=args)
    )
    assert resp.status_code == 302
    application_accepted = Application.objects.get(id=application_accepted.id)
    assert application_accepted.rsvp_status == Application.RSVP_WAITING


def test_changing_application_rsvp(
        admin_client, future_event, application_submitted):
    assert application_submitted.rsvp_status == Application.RSVP_WAITING
    resp = admin_client.post(
        reverse('applications:change_rsvp', args=[future_event.page_url]),
        {'rsvp_status': Application.RSVP_YES, 'application': application_submitted.id}
    )
    assert resp.status_code == 200
    application_submitted = Application.objects.get(id=application_submitted.id)
    assert application_submitted.rsvp_status == Application.RSVP_YES


def test_changing_application_status_errors(
        client, admin_client, future_event, application_submitted):
    # user without permissions:
    resp = client.post(
        reverse('applications:change_state', args=[future_event.page_url]),
        {'state': 'accepted', 'application': application_submitted.id}
    )
    assert resp.status_code == 302

    # lack of state parameter
    resp = admin_client.post(
        reverse('applications:change_state', args=[future_event.page_url]),
        {'application': application_submitted.id}
    )
    assert 'error' in resp.json()

    # lack of application parameter
    resp = admin_client.post(
        reverse('applications:change_state', args=[future_event.page_url]),
        {'state': 'accepted'}
    )
    assert 'error' in resp.json()


def test_changing_application_rsvp_errors(
        client, admin_client, future_event, application_submitted):
    # user without permissions:
    resp = client.post(
        reverse('applications:change_rsvp', args=[future_event.page_url]),
        {'rsvp_status': Application.RSVP_YES, 'application': application_submitted.id}
    )
    assert resp.status_code == 302

    # lack of rsvp_status parameter
    resp = admin_client.post(
        reverse('applications:change_rsvp', args=[future_event.page_url]),
        {'application': application_submitted.id}
    )
    assert 'error' in resp.json()

    # lack of application parameter
    resp = admin_client.post(
        reverse('applications:change_rsvp', args=[future_event.page_url]),
        {'rsvp_status': Application.RSVP_YES}
    )
    assert 'error' in resp.json()


def test_changing_application_status_in_bulk(
        admin_client, future_event, application_submitted, application_rejected):
    assert application_submitted.state == 'submitted'
    assert application_rejected.state == 'rejected'
    resp = admin_client.post(
        reverse('applications:change_state', args=[future_event.page_url]),
        {'state': 'accepted', 'application': [application_submitted.id, application_rejected.id]}
    )
    assert resp.status_code == 200
    application_submitted = Application.objects.get(id=application_submitted.id)
    application_rejected = Application.objects.get(id=application_rejected.id)
    assert application_submitted.state == 'accepted'
    assert application_rejected.state == 'accepted'


@pytest.mark.xfail(reason="TODO")
def test_application_scores_is_queried_once(
        admin_client, future_event_form, future_event, admin_user):

    Application.objects.bulk_create(
        Application(form=future_event_form, email=f"foo+{i}@email.com")
        for i in range(5)
    )

    # For every application, create a random score
    for application in Application.objects.filter(form=future_event_form):
        Score.objects.create(user=admin_user, application=application, score=random.randint(1, 5))

    applications_url = reverse('applications:applications', kwargs={'city': future_event.page_url})

    with CaptureQueriesContext(connection) as queries:
        admin_client.get(applications_url)

    score_queries = [q for q in queries.captured_queries if 'applications_score' in q['sql']]
    # We want to query the scores only once when accessing the view
    assert len(score_queries) == 1
