import pytest

from applications.models import Application, Score
from applications.services import get_applications_for_event
from core.models import User


@pytest.fixture
def scores_by_other_users(future_event_form):
    user = User.objects.create(email="user-1@test.com")
    another_user = User.objects.create(email="user-2@test.com")
    for i, app in enumerate(Application.objects.filter(form=future_event_form)):
        # Add some randomization
        Score.objects.create(application=app, user=user, score=1 if i % 2 == 0 else 4)
        Score.objects.create(application=app, user=another_user, score=2 if i % 2 == 0 else 5)


def test_it_sorts_applications_by_score_excluding_hidden(
    future_event, scored_applications, admin_user, scores_by_other_users
):
    """Tests if, when the user sorts the applications by average score, we don't include the ones they
    haven't scored yet.

    For example, consider [these applications](https://cln.sh/JAoo8H) sorted by average score with the
    previous implementation. We know #1 is higher than 4.375 and #3 is lower than 4.375 and higher than
    4.25 just because of the sorting."""

    # Delete some of the scores given by the admin user so we can test the sorting
    Score.objects.filter(
        user=admin_user, application__in=scored_applications, pk__gt=scored_applications.count() / 2
    ).delete()

    apps = get_applications_for_event(event=future_event, user=admin_user, order="-average_score")
    result = [(app.was_scored_by_user, round(app.average_score, 3)) for app in apps]
    assert result == [
        (True, 3.667),
        (True, 1.333),
        (False, 4.5),
        (False, 1.5),
        (False, 1.5),
    ]

    # Check if the sorting doesn't break if we don't pass `user`
    apps = get_applications_for_event(event=future_event, order="-average_score")
    result = [(app.was_scored_by_user, round(app.average_score, 3)) for app in apps]
    assert result == [(False, 4.5), (False, 3.667), (False, 1.5), (False, 1.5), (False, 1.333)]
