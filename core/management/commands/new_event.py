# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import djclick as click
from django.conf import settings
from django.template.loader import render_to_string
from slacker import Error as SlackerError

from core.command_helpers import gather_event_date_from_prompt
from core.default_eventpage_content import (get_default_eventpage_data,
                                            get_default_menu)
from core.forms import AddOrganizerForm
from core.models import Event, EventPageContent, EventPageMenu
from core.slack_client import slack
from core.utils import get_coordinates_for_city

DELIMITER = "\n-------------------------------------------------------------\n"


def get_basic_info():
    """
        Here we're asking the user for:
        - city
        - country
        - date
        - url
        - event_email
        And return all these information.
    """
    click.echo(
        "Hello there! Let's create new Django Girls event! So exciting!")
    click.echo("Let's start with some basics.")
    city = click.prompt(click.style(
        "What is the name of the city?", bold=True, fg='yellow'))
    country = click.prompt(click.style(
        "What is the name of the country?", bold=True, fg='yellow'))

    date = gather_event_date_from_prompt()

    url = click.prompt(click.style(
        "What should be the URL of website? djangogirls.org/xxxx", bold=True, fg='yellow'))
    event_mail = click.prompt(click.style(
        "What is the mail adress of the event? xxxx@djangogirls.org", bold=True, fg='yellow'))
    click.echo("Ok, got that! Your new event will happen in {0}, {1} on {2}".format(
        city, country, date))

    return (city, country, date, url, event_mail)


def get_main_organizer():
    """
        We're asking user for name and address of main organizer, and return
        a list of dictionary.
    """
    team = []
    click.echo("Now let's talk about the team. First the main organizer:")
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
        form = AddOrganizerForm(data=member)
        user = form.save()
        members.append(user)
    return members


def add_default_content(event):
    """
        Populate EventPageContent with default layout
    """
    data = get_default_eventpage_data()

    i = 0
    for section in data:
        section['event'] = event
        section['position'] = i
        section['content'] = render_to_string(section['template'])
        del section['template']
        EventPageContent.objects.create(**section)
        i += 1


def add_default_menu(event):
    """
        Populate EventPageMenu with default links
    """
    data = get_default_menu()

    i = 0
    for link in data:
        link['event'] = event
        link['position'] = i
        EventPageMenu.objects.create(**link)
        i += 1


def brag_on_slack_bang(city, country, team):
    """
        This is posting a message about Django Girls new event to #general channel on Slack!
    """
    text = ':django_pony: :zap: Woohoo! :tada: New Django Girls alert! Welcome Django Girls {city}, {country}. Congrats {team}!'.format(
        city=city, country=country, team=', '.join(
            ['{} {}'.format(x.first_name, x.last_name) for x in team])
    )
    slack.chat.post_message(
        channel='#general',
        text=text,
        username='Django Girls',
        icon_emoji=':django_heart:'
    )


@click.command()
@click.option('--short', '-s', is_flag=True, help="Shorter version of the setup email to use with a canned email.")
def command(short):
    """Creates new Django Girls event"""
    # Basics
    (city, country, date, url, event_mail) = get_basic_info()

    # Main organizer
    main_organizer = get_main_organizer()

    # Team
    team = get_team(main_organizer)

    click.echo("OK! That's it. Now I'll create your event.")

    # Event and EventPage objects
    name = 'Django Girls ' + city
    latlng = get_coordinates_for_city(city, country)
    mail = event_mail + '@djangogirls.org'
    event = Event.objects.create(
        name=name, city=city, country=country,
        latlng=latlng, email=mail, date=date,
        is_on_homepage=False, page_url=url, page_title=name)

    # Create users
    members = create_users(team, event)
    event.main_organizer = members[0]
    event.save()

    # Default content
    add_default_content(event)
    add_default_menu(event)

    click.secho(
        "Website is ready here: http://djangogirls.org/{0}".format(url),
        fg='green')
    click.echo(DELIMITER)

    click.secho("Ok, now follow this:", fg='black', bg='green')
    click.echo(
        "1. Find a photo of a city with CC license on Flickr. Download it.")
    click.echo(
        "2. Go here: http://djangogirls.org/admin/core/event/{0}/".format(event.id))
    click.echo(
        "3. Upload a photo of city, add credits and tick 'is on homepage' checkbox. Save.")
    click.echo("4. Send e-mail with instructions to a team!")
    click.echo(DELIMITER)
    click.secho(
        "This is a ready, filled out mail to sent to organizers:", fg='green')

    click.echo("SUBJECT: Django Girls {} setup".format(event.city))
    click.echo("TO: {}, {}, hello@djangogirls.org".format(
        ', '.join([x.email for x in members]),
        event.email
    ))
    click.echo("BODY:")

    if short:
        click.echo(render_to_string('emails/setup-short.txt', {
            'event': event,
        }))
    else:
        click.echo(render_to_string('emails/setup.txt', {
            'event': event,
            'email_password': 'UNDEFINED',
            'settings': settings
        }))

    brag_on_slack_bang(city, country, members)
