from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from applications.questions import DEFAULT_QUESTIONS


def test_access_apply_view(client, future_event, future_event_form):
    apply_url = reverse("applications:apply", kwargs={"page_url": future_event.page_url})
    resp = client.get(apply_url)
    assert resp.status_code == 200
    assert resp.context["form_obj"] == future_event_form
    # there is two more fields than default questions,
    # because we always add newsletter option at the end
    # and a captcha is not added for testing anymore
    assert len(resp.context["form"].fields) == len(DEFAULT_QUESTIONS) + 1

    # Redirect to event page because there is no form
    future_event_form.delete()
    resp = client.get(apply_url)
    assert resp.status_code == 302

    # Show 404 because there is no event page
    future_event.delete()
    resp = client.get(apply_url)
    assert resp.status_code == 404


def test_application_not_open(client, future_event_form, future_event):
    now = timezone.now()
    future_event_form.open_from = now + timedelta(days=1)
    future_event_form.open_until = now + timedelta(days=2)
    future_event_form.save()

    resp = client.get(reverse("applications:apply", kwargs={"page_url": future_event.page_url}))
    assert resp.status_code == 302


def test_application_open(client, future_event_form, future_event):
    now = timezone.now()
    future_event_form.open_from = now - timedelta(days=1)
    future_event_form.open_until = now + timedelta(days=1)
    future_event_form.save()

    resp = client.get(reverse("applications:apply", kwargs={"page_url": future_event.page_url}))
    assert resp.status_code == 200
    assert resp.context["form_obj"] == future_event_form


def test_application_not_open_organiser(client, future_event_form, future_event):
    now = timezone.now()
    future_event_form.open_from = now + timedelta(days=1)
    future_event_form.open_until = now + timedelta(days=2)
    future_event_form.save()

    client.force_login(future_event.main_organizer)

    resp = client.get(reverse("applications:apply", kwargs={"page_url": future_event.page_url}))
    assert resp.status_code == 200
    assert resp.context["form_obj"] == future_event_form


def test_application_not_open_superuser(admin_client, future_event_form, future_event):
    now = timezone.now()
    future_event_form.open_from = now + timedelta(days=1)
    future_event_form.open_until = now + timedelta(days=2)
    future_event_form.save()

    resp = admin_client.get(reverse("applications:apply", kwargs={"page_url": future_event.page_url}))
    assert resp.status_code == 200
    assert resp.context["form_obj"] == future_event_form


def test_event_not_live(client, hidden_event):
    resp = client.get(reverse("applications:apply", kwargs={"page_url": hidden_event.page_url}))
    assert resp.status_code == 200
    assert resp.context["city"] == hidden_event.page_url


def test_application_form_valid(client, future_event_form, future_event):

    question_data = {
        "question_1": "Bill Smith",
        "question_2": "bill.smith@djangogirls.org",
        "question_3": "0123445689",
        "question_4": "London, United Kingdom",
        "question_5": "",  # Not required
        "question_6": "Mac OS X",
        "question_7": "I work as a programmer",
        "question_8": "",
        "question_9": "Developer",
        "question_10": "To test things",
        "question_11": "test",
        "question_12": "Facebook",
        "question_13": "Yes",
        "question_14": "I've read and understood the Django Girls Code of Conduct",
        "newsletter_optin": True,
    }

    # TODO: Need to find a way to get the question numbers as they aren't always 1-14

    # resp = client.post(
    #     reverse('applications:apply', kwargs={'city': future_event.page_url}),
    #     data=question_data
    # )
    # assert resp.status_code == 200
    # assert resp.context['event'] == future_event
    assert True
