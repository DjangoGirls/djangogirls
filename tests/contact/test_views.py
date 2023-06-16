from django.urls import reverse

from contact.models import ContactEmail

CONTACT_URL = "contact:landing"


def test_contact_page_loads(client):
    resp = client.get(reverse(CONTACT_URL))
    assert resp.status_code == 200


def test_form_sends_email_to_support(client, mailoutbox):
    post_data = {
        "name": "test name",
        "message": "nice message",
        "email": "lord@dracula.trans",
        "contact_type": ContactEmail.SUPPORT,
        "g-recaptcha-response": "PASSED",
    }
    resp = client.post(reverse(CONTACT_URL), data=post_data)

    assert len(mailoutbox) == 1
    email = mailoutbox[0]

    assert email.to == ["hello@djangogirls.org"]
    assert email.reply_to == ["test name <lord@dracula.trans>"]
    assert email.body == "nice message"


def test_form_sends_email_to_chapter(client, mailoutbox, future_event):
    future_event.email = "test@test.com"
    future_event.save()

    post_data = {
        "name": "test name",
        "message": "nice message",
        "email": "lord@dracula.trans",
        "contact_type": ContactEmail.CHAPTER,
        "event": future_event.pk,
        "g-recaptcha-response": "PASSED",
    }
    resp = client.post(reverse(CONTACT_URL), data=post_data)
    assert resp.status_code == 302
    assert len(mailoutbox) == 1
    email = mailoutbox[0]

    assert email.to == ["test@test.com"]
    assert email.reply_to == ["test name <lord@dracula.trans>"]
    assert email.body == "nice message"


def test_chapter_contact_requires_event(client, mailoutbox):
    post_data = {
        "name": "test name",
        "message": "nice message",
        "email": "lord@dracula.trans",
        "contact_type": ContactEmail.CHAPTER,
        "event": "",
    }
    resp = client.post(reverse(CONTACT_URL), data=post_data)
    assert resp.status_code == 200
    assert len(mailoutbox) == 0
    assert "event" in resp.context["form"].errors
    assert ContactEmail.objects.exists() is False


def test_message_with_links_fails(client, mailoutbox, future_event):
    future_event.email = "test@test.com"
    future_event.save()

    post_data = {
        "name": "test name",
        "message": 'nice message <a href="#">test link</a>',
        "email": "lord@dracula.trans",
        "contact_type": ContactEmail.CHAPTER,
        "event": future_event.pk,
        "g-recaptcha-response": "PASSED",
    }
    resp = client.post(reverse(CONTACT_URL), data=post_data)
    assert resp.status_code == 302
    assert len(mailoutbox) == 1
    contact_email = ContactEmail.objects.first()
    assert contact_email is not None
    assert '<a href="#">' not in contact_email.message


def test_email_is_saved_into_database(client, mailoutbox, future_event):
    assert ContactEmail.objects.exists() is False

    post_data = {
        "name": "test name",
        "message": "nice message",
        "email": "lord@dracula.trans",
        "contact_type": ContactEmail.CHAPTER,
        "event": future_event.pk,
        "g-recaptcha-response": "PASSED",
    }
    resp = client.post(reverse(CONTACT_URL), data=post_data)
    assert resp.status_code == 302
    assert len(mailoutbox) == 1
    assert ContactEmail.objects.count() == 1

    contact_email = ContactEmail.objects.first()
    assert contact_email.name == "test name"
    assert contact_email.sent_to == future_event.email
    assert contact_email.message == "nice message"
    assert contact_email.email == "lord@dracula.trans"
    assert contact_email.event == future_event
    assert contact_email.contact_type == ContactEmail.CHAPTER
