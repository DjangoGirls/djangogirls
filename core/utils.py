from datetime import datetime
import requests

from django.utils import timezone
from django_date_extensions.fields import ApproximateDate

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
    except:
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


def get_approximate_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%d/%m/%Y')
        return ApproximateDate(year=date_obj.year, month=date_obj.month, day=date_obj.day)
    except ValueError:
        try:
            date_obj = datetime.strptime(date_str, '%m/%Y')
            return ApproximateDate(year=date_obj.year, month=date_obj.month)
        except ValueError:
            return False
    return False
