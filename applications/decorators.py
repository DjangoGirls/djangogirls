from functools import wraps

from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from core.utils import get_event


def organiser_only(function):
    """
    Decorator for views that checks that the user is logged in and that
    they are a team member for a particular event. Returns 404 otherwise.
    """

    @wraps(function)
    def decorator(request, *args, **kwargs):
        page_url = kwargs.get("page_url")

        if not page_url:
            raise ValueError(_('"page_url" slug must be present to user this decorator.'))

        if not request.user.is_authenticated:
            return redirect("core:event", page_url)

        event = get_event(page_url, request.user.is_authenticated, False)
        if event and (request.user in event.team.all() or request.user.is_superuser):
            return function(request, *args, **kwargs)
        return HttpResponseNotFound()

    return decorator
