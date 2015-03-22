from functools import wraps

from core.utils import get_event_page

from django.http import HttpResponseNotFound


def organiser_only(function):
    """
    Decorator for views that checks that the user is logged in and that
    they are a team member for a particular page. Returns 404 otherwise.
    """

    @wraps(function)
    def decorator(request, *args, **kwargs):
        if not kwargs.get('city'):
            raise ValueError(
                '"City" slug must be present to user this decorator.')

        if not request.user.is_authenticated():
            return HttpResponseNotFound()

        city = kwargs.get('city')
        page = get_event_page(city, request.user.is_authenticated(), False)
        if request.user in page.event.team.all() or request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseNotFound()
    return decorator
