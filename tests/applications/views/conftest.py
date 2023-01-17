import pytest

from applications.models import Answer, Application


@pytest.fixture
def application_submitted(future_event_form):
    application = Application.objects.create(form=future_event_form, state="submitted")
    last_question = future_event_form.question_set.last()
    Answer.objects.create(application=application, question=last_question, answer="answer to last for app 1")
    return application


@pytest.fixture
def application_accepted(future_event_form):
    return Application.objects.create(form=future_event_form, state="accepted")


@pytest.fixture
def application_rejected(future_event_form):
    return Application.objects.create(form=future_event_form, state="rejected")


@pytest.fixture
def application_waitlisted(future_event_form):
    return Application.objects.create(form=future_event_form, state="waitlisted")


@pytest.fixture
def applications(application_submitted, application_accepted, application_rejected, application_waitlisted):
    return [application_submitted, application_accepted, application_rejected, application_waitlisted]
