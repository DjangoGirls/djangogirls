import pytest

from applications.models import Application, Email, Form
from core.models import Event, User


@pytest.fixture
def event(db):
    return Event.objects.create(name="Test", city="Test", country="Test", is_page_live=True, page_url="test")


@pytest.fixture
def form(db, event):
    return Form.objects.create(event=event)


@pytest.fixture
def user(db):
    return User.objects.create(email="test@test.com")


@pytest.fixture
def another_user(db):
    return User.objects.create(email="test2@test.com")


@pytest.fixture
def application(db, form):
    return Application.objects.create(form=form)


@pytest.fixture
def accepted_application(db, form):
    return Application.objects.create(email="recipient@email.com", form=form, state="accepted")


@pytest.fixture
def email(db, form, user):
    return Email.objects.create(
        form=form,
        author=user,
        subject="Test",
        text="Hey! [rsvp-url-yes] [rsvp-url-no] Bye",
        recipients_group="accepted",
    )
