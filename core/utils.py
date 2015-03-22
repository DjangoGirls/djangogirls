import requests

from django.utils import timezone
from django_date_extensions.fields import ApproximateDate

from applications.models import Form
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


def get_applications_for_page(page, state=None):
    """
    Return a QuerySet of Application objects for a given page.
    Raises Form.DoesNotExist if Form for page does not yet exist.
    """
    page_form = Form.objects.filter(page=page)
    if not page_form.exists():
        raise Form.DoesNotExist
    page_form = page_form.first()
    if state:
        return page_form.application_set.filter(state__in=state)
    return page_form.application_set.all()
