from django.db.models import Exists, OuterRef

from applications.models import Application, Event, Score
from core.models import User


def get_applications_for_event(event, state=None, rsvp_status=None, order=None, user: User = None):
    """
    Return a QuerySet of Application objects for a given event.
    Raises Form.DoesNotExist if Form for event does not yet exist.
    """

    applications = (
        Application.objects.filter(form__event=event)
        .order_by("id")
        .select_related("form")
        .prefetch_related("answer_set", "scores", "scores__user", "form__event", "scores__application")
    )

    scores_subquery = Score.objects.filter(application=OuterRef("pk"), user=user)
    applications = applications.annotate(was_scored_by_user=Exists(scores_subquery))

    if rsvp_status:
        applications = applications.filter(state="accepted", rsvp_status__in=rsvp_status)
    elif state:
        applications = applications.filter(state__in=state)

    if order:
        is_reversed = True if order[0] == "-" else False
        order = order[1:] if order[0] == "-" else order
        if order == "average_score":
            # here is an exception for the average_score, because we also want to get
            # the standard deviation into account in this sorting
            applications = sorted(
                applications,
                key=lambda app: (app.was_scored_by_user, getattr(app, order), -app.stdev()),
                reverse=is_reversed,
            )
        else:
            applications = sorted(applications, key=lambda app: getattr(app, order), reverse=is_reversed)

    return applications


def get_random_application(user: User, event: Event, prev_application: Application):
    """
    Get a new random application for a particular event,
    that hasn't been scored by the user.
    """
    return (
        Application.objects.filter(form__event=event)
        .exclude(
            pk=prev_application.id,
        )
        .exclude(scores__user=user)
        .order_by("?")
        .first()
    )
