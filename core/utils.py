import requests

from django.utils import timezone
from django_date_extensions.fields import ApproximateDate

from applications.models import Application, Form
from .models import EventPage

def get_coordinates_for_city(city, country):

    q = '{0}, {1}'.format(city.encode('utf-8'), country.encode('utf-8'))
    req = requests.get(
        'http://nominatim.openstreetmap.org/search',
        params={'format': 'json', 'q': q}
    )

    try:
        data = req.json()[0]
        return '{0}, {1}'.format(data['lat'], data['lon'])
    except IndexError:
        return None


def get_event_page(city, is_user_authenticated, is_preview):
    now = timezone.now()
    now_approx = ApproximateDate(year=now.year, month=now.month, day=now.day)
    try:
        page = EventPage.objects.get(url=city)
    except EventPage.DoesNotExist:
        return None

    if not (is_user_authenticated or is_preview) and not page.is_live:
        past = page.event.date <= now_approx
        return (city, past)

    return page


def get_applications_for_page(page, state=None, rsvp_status=None, order=None):
    """
    Return a QuerySet of Application objects for a given page.
    Raises Form.DoesNotExist if Form for page does not yet exist.
    """
    page_form = Form.objects.filter(page=page)
    if not page_form.exists():
        raise Form.DoesNotExist
    page_form = page_form.first()

    applications = page_form.application_set.all()

    if rsvp_status: 
        applications = applications.filter(state='accepted', rsvp_status__in=rsvp_status)
    elif state:
        applications = applications.filter(state__in=state)

    if order:
        is_reversed = True if order[0] == '-' else False
        order = order[1:] if order[0] == '-' else order
        if order == 'average_score':
            # here is an exception for the average_score, because we also want to get
            # the standard deviation into account in this sorting
            applications = sorted(applications, key=lambda app: (getattr(app, order), -app.stdev()), reverse=is_reversed)
        else:
            applications = sorted(applications, key=lambda app: getattr(app, order), reverse=is_reversed)

    return applications


def random_application(request, page, prev_application):
    """
    Get a new random application for a particular event,
    that hasn't been scored by the request user.
    """
    return Application.objects.filter(
        form__page=page
        ).exclude(pk=prev_application.id
        ).exclude(scores__user=request.user).order_by('?').first()
