from datetime import timedelta

from django.utils import timezone

from applications.models import Form
from applications.questions import DEFAULT_QUESTIONS


def test_adding_default_questions(event):
    # Each new form should automatically create default questions
    form = Form.objects.create(event=event)
    assert form.question_set.count() == len(DEFAULT_QUESTIONS)

    # If you update the form, the default questions shouldn't be added
    form.text_header = "Test"
    form.save()
    assert form.question_set.count() == len(DEFAULT_QUESTIONS)


def test_no_application_dates(event):
    form = Form.objects.create(event=event)
    assert form.application_open is True


def test_application_open(event):
    now = timezone.now()
    form = Form.objects.create(event=event, open_from=now - timedelta(days=1), open_until=now + timedelta(days=1))
    assert form.application_open is True


def test_application_in_future(event):
    now = timezone.now()
    form = Form.objects.create(event=event, open_from=now + timedelta(days=1), open_until=now + timedelta(days=2))
    assert form.application_open is False


def test_application_closed(event):
    now = timezone.now()
    form = Form.objects.create(event=event, open_from=now - timedelta(days=2), open_until=now - timedelta(days=1))
    assert form.application_open is False
