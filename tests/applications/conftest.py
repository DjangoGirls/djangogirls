import pytest

from applications.models import Application, Form, Score


@pytest.fixture
def future_event_form(future_event):
    return Form.objects.create(event=future_event)


@pytest.fixture
def scored_applications(future_event_form, admin_user):
    Application.objects.bulk_create(Application(form=future_event_form, email=f"foo+{i}@email.com") for i in range(5))

    applications = Application.objects.filter(form=future_event_form)

    for i, application in enumerate(applications):
        Score.objects.create(user=admin_user, application=application, score=i + 1)

    return applications
