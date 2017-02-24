# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import djclick as click

from core.command_helpers import gather_event_date_from_prompt
from core.models import Event
from core.utils import get_main_organizer, get_team, create_users


def get_event(id_str):
    try:
        return Event.objects.get(id=int(id_str))
    except (ValueError, Event.DoesNotExist):
        return False


def gather_information():
    click.echo("Hello there sunshine! We're gonna copy an event website now.")

    event = get_event(
        click.prompt(click.style("First, give me the latest ID of the Event "
        "object you want to copy", bold=True, fg='yellow'))
    )

    while not event:
        event = get_event(click.prompt("Wrong ID! Try again"))

    number = click.prompt(click.style("What is the number of the event in this city? "
        "If this is a second event, write 2. If third, then 3. You got it", bold=True, fg='yellow')
    )

    date = gather_event_date_from_prompt()

    new_team = click.confirm(click.style(
        "Do you need to change the whole team?", bold=True, fg='yellow'), default=False
    )

    return (event, number, date, new_team)


@click.command()
def command():
    """Duplicates Django Girls event with a new date"""

    # Gather data
    (event, number, date, new_team) = gather_information()
    organizers = event.team.all()

    # Remove #{no} from name:
    name = event.name.split('#')[0].strip()
    number = int(number)
    event_id = event.id

    # Change the name of previous event to {name} #{number-1}
    event.name = "{} #{}".format(name, number-1)
    event.save()

    # Copy event with a name {name} #{number}, new date and empty stats
    new_event = event
    new_event.pk = None
    new_event.name = "{} #{}".format(name, number)
    new_event.date = date
    new_event.is_page_live = False
    new_event.attendees_count = None
    new_event.applicants_count = None
    new_event.save()

    # Copy or change organizers
    if new_team:
        main_organizer = get_main_organizer()
        team = get_team(main_organizer)
        members = create_users(team, new_event)
        new_event.main_organizer = members[0]
    else:
        new_event.team = organizers

    # Change the title and url of previous event page
    event.page_title = "{} #{}".format(name, number-1)
    event.page_url = "{}{}".format(event.page_url, number-1)
    event.save()

    event = Event.objects.get(id=event_id)

    # Copy all EventPageContent objects
    for obj in event.content.all():
        new_content = obj
        new_content.id = None
        new_content.event = new_event
        new_content.save()

        new_content.coaches = obj.coaches.all()
        new_content.sponsors = obj.sponsors.all()

    # Copy all EventPageMenu objects
    for obj in event.menu.all():
        new_obj = obj
        new_obj.pk = None
        new_obj.event = new_event
        new_obj.save()

    click.echo(click.style("Website is ready here: http://djangogirls.org/{0}".format(new_event.page_url),
    bold=True, fg="green"))
    click.echo("Congrats on yet another event!")
