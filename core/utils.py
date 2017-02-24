from datetime import date, datetime, timedelta

import requests
from django.utils import timezone
from django_date_extensions.fields import ApproximateDate
import djclick as click

from .models import Event
from .forms import AddOrganizerForm

NOMINATIM_URL = 'http://nominatim.openstreetmap.org/search'


def get_coordinates_for_city(city, country):
    q = '{0}, {1}'.format(city, country)
    req = requests.get(
        NOMINATIM_URL,
        params={'format': 'json', 'q': q}
    )

    try:
        data = req.json()[0]
        return '{0}, {1}'.format(data['lat'], data['lon'])
    except (IndexError, KeyError):
        return None


def get_event(city, is_user_authenticated, is_preview):
    now = timezone.now()
    now_approx = ApproximateDate(year=now.year, month=now.month, day=now.day)
    try:
        event = Event.objects.get(page_url=city)
    except Event.DoesNotExist:
        return None

    if not (is_user_authenticated or is_preview) and not event.is_page_live:
        past = event.date <= now_approx
        return (city, past)

    return event


def get_approximate_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%d/%m/%Y')
        return ApproximateDate(year=date_obj.year, month=date_obj.month, day=date_obj.day)
    except ValueError:
        try:
            date_obj = datetime.strptime(date_str, '%m/%Y')
            return ApproximateDate(year=date_obj.year, month=date_obj.month)
        except ValueError:
            return None
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

# Get organizers info functions used in 'new_event' and 'copy_event' management commands.

def get_main_organizer():
    """
        We're asking user for name and address of main organizer, and return
        a list of dictionary.
    """
    team = []
    click.echo("Let's talk about the team. First the main organizer:")
    main_name = click.prompt(click.style(
        "First and last name", bold=True, fg='yellow'))
    main_email = click.prompt(click.style(
        "E-mail address", bold=True, fg='yellow'))

    team.append({'name': main_name, 'email': main_email})

    click.echo(u"All right, the main organizer is {0} ({1})".format(
        main_name, main_email))

    return team

def get_team(team):
    """
        We're asking user for names and address of the rest of the team,
        and append that to a list we got from get_main_organizer
    """
    add_team = click.confirm(click.style(
        "Do you want to add additional team members?", bold=True, fg='yellow'), default=False)
    i = 1
    while add_team:
        i += 1
        name = click.prompt(click.style(
            "First and last name of #{0} member".format(i), bold=True, fg='yellow'))
        email = click.prompt(click.style(
            "E-mail address of #{0} member".format(i), bold=True, fg='yellow'))
        if len(name) > 0:
            team.append({'name': name, 'email': email})
            click.echo("All right, the #{0} team member of Django Girls is {1} ({2})".format(
                i, name, email))
        add_team = click.confirm(click.style(
            "Do you want to add additional team members?", bold=True, fg='yellow'), default=False)

    return team


def create_users(team, event):
    """
        Create or get User objects based on team list
    """
    members = []
    for member in team:
        member['event'] = event.pk
        form = AddOrganizerForm(member)
        user = form.save()
        members.append(user)
    return members
