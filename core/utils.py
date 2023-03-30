from datetime import date, datetime, timedelta

import requests
from django.utils import timezone
from django_date_extensions.fields import ApproximateDate

from .models import Event

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


def get_coordinates_for_city(city, country):
    q = f"{city}, {country}"
    req = requests.get(NOMINATIM_URL, params={"format": "json", "q": q})

    try:
        data = req.json()[0]
        return f'{data["lat"]}, {data["lon"]}'
    except (IndexError, KeyError):
        return None


def get_event(page_url, is_user_authenticated, is_preview):
    now = timezone.now()
    now_approx = ApproximateDate(year=now.year, month=now.month, day=now.day)
    try:
        event = Event.objects.get(page_url=page_url)
    except Event.DoesNotExist:
        return None
    except Event.MultipleObjectsReturned:
        event = Event.objects.filter(page_url=page_url).order_by("-date").first()

    if not (is_user_authenticated or is_preview) and not event.is_page_live:
        past = event.date <= now_approx
        return page_url, past

    return event


def get_approximate_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        return ApproximateDate(year=date_obj.year, month=date_obj.month, day=date_obj.day)
    except ValueError:
        try:
            date_obj = datetime.strptime(date_str, "%m/%Y")
            return ApproximateDate(year=date_obj.year, month=date_obj.month)
        except ValueError:
            return None


def next_sunday(day):
    """
    Return a date object corresponding to the next Sunday after the given date.
    If the given date is a Sunday, return the Sunday next week.
    """
    if day.weekday() == 6:  # sunday
        return day + timedelta(days=7)
    else:
        return day + timedelta(days=(6 - day.weekday()))


def next_deadline():
    """
    Return the next deadline when we need to send invoices to GitHub.
    Deadlines are every second Sunday, starting from September 4th 2016.
    """

    today = date.today()

    days_since_starting_sunday = (today - date(2016, 9, 4)).days

    if days_since_starting_sunday % 14 < 7:
        return next_sunday(next_sunday(today))
    else:
        return next_sunday(today)
