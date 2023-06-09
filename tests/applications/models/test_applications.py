import pytest
from django.db import IntegrityError

from applications.models import Application, Score


def test_email_page_unique(form):
    Application.objects.create(form=form, email="test@test.pl")
    assert form.application_set.count() == form.number_of_applications
    assert form.number_of_applications == 1

    with pytest.raises(IntegrityError):
        Application.objects.create(form=form, email="test@test.pl")


def test_number_of_applications(form):
    assert form.application_set.count() == form.number_of_applications

    Application.objects.create(form=form)
    assert form.application_set.count() == form.number_of_applications
    assert form.number_of_applications == 1


def test_average_score(application, user, another_user):
    assert application.average_score != 4

    score_1 = Score.objects.create(user=user, application=application, score=3)
    score_2 = Score.objects.create(user=another_user, application=application, score=5)

    assert application.average_score == 4


def test_generating_code(application):
    assert len(application.generate_code()) == 24


def test_get_rsvp_yes_code(application):
    assert application.rsvp_yes_code is None
    rsvp_code = application.get_rsvp_yes_code()
    assert len(rsvp_code) == 24
    assert application.rsvp_yes_code == rsvp_code

    # Make sure it doesn't generate again:
    assert application.get_rsvp_yes_code() == rsvp_code


def test_get_rsvp_no_code(application):
    assert application.rsvp_no_code is None
    rsvp_code = application.get_rsvp_no_code()
    assert len(rsvp_code) == 24
    assert application.rsvp_no_code == rsvp_code

    # Make sure it doesn't generate again:
    assert application.get_rsvp_no_code() == rsvp_code


def test_get_by_rsvp_code(application, event):
    rsvp_code_no = application.get_rsvp_no_code()
    rsvp_code_yes = application.get_rsvp_yes_code()

    assert Application.get_by_rsvp_code(rsvp_code_yes, event) == (application, "yes")
    assert Application.get_by_rsvp_code(rsvp_code_no, event) == (application, "no")
    assert Application.get_by_rsvp_code("notexisting", event) == (None, None)


def test_is_accepted(application):
    for state in Application.APPLICATION_STATES:
        application.state = state[0]
        application.save()

        is_accepted = True if state[0] == "accepted" else False
        assert application.is_accepted == is_accepted


def test_is_scored_by_user(application, user, another_user):
    Score.objects.create(user=user, application=application, score=3)

    assert application.is_scored_by_user(user) is True
    assert application.is_scored_by_user(another_user) is False

    Score.objects.create(user=another_user, application=application, score=0)
    assert application.is_scored_by_user(another_user) is False
