# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import djclick as click
from django.conf import settings
from django.template.loader import render_to_string

from ...command_helpers import gather_event_date_from_prompt
from ...forms import AddOrganizerForm, EventForm
from ...models import Event
from ...utils import get_coordinates_for_city

from slack_client.utils import get_connection as get_slack_connection

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
        "What should be the URL of website? djangogirls.org/______", bold=True, fg='yellow'))
    event_mail = click.prompt(click.style(
        "What is the email prefix of the event? ______@djangogirls.org", bold=True, fg='yellow'),
        default=url)
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


def brag_on_slack_bang(city, country, team):
    """
        This is posting a message about Django Girls new event to #general channel on Slack!
    """
    text = ':django_pony: :zap: Woohoo! :tada: New Django Girls alert! Welcome Django Girls {city}, {country}. Congrats {team}!'.format(
        city=city, country=country, team=', '.join(
            ['{} {}'.format(x.first_name, x.last_name) for x in team])
    )
    conn = get_slack_connection()
    conn.chat.post_message(
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
    (city, country, date, url, event_email) = get_basic_info()

    # Main organizer
    main_organizer = get_main_organizer()

    # Team
    team = get_team(main_organizer)

    click.echo("OK! That's it. Now I'll create your event.")

    # Event and EventPage objects
    name = 'Django Girls ' + city
    latlng = get_coordinates_for_city(city, country)
    email = event_email + '@djangogirls.org'
    form = EventForm({
        'city': city,
        'country': country,
        'date': date,
        'email': email,
        'latlng': latlng,
        'name': name,
        'page_title': name,
        'page_url': url})
    if not form.is_valid():
        click.secho(
            "OOPS! Something went wrong!", fg='red')
        for field, errors in form.errors.items():
            for error in errors:
                click.secho(
                    "    {field:10} {error}".format(error=error, field=field),
                    fg='red')
        return
    event = form.save()

    # Create users
    members = create_users(team, event)
    event.main_organizer = members[0]
    event.save()

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
