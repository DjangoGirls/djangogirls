# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import djclick as click

from core.command_helpers import gather_event_date_from_prompt
from core.models import Event, EventPage


def get_event(id_str):
    try:
        return Event.objects.get(id=int(id_str))
    except (ValueError, Event.DoesNotExist):
        return False


def gather_information():
    click.echo("Hello there sunshine! We're gonna copy an event website now.")

    event = get_event(
        click.prompt(
            "First, give me the ID of the Event object we're gonna copy. "
            "Don't mix it up with EventPage object. If there is more than "
            "one event in this city already, give me ID of the latest one"
        )
    )

    while not event:
        event = get_event(click.prompt("Wrong ID! Try again"))

    number = click.prompt(
        "What is the number of the event in this city? "
        "If this is a second event, write 2. If third, then 3. You got it"
    )

    date = gather_event_date_from_prompt()

    return (event, number, date)


@click.command()
def command():
    """Duplicates Django Girls event with a new date"""

    # Gather data
    (event, number, date) = gather_information()
    eventpage = event.eventpage
    previous_url = "/{}".format(eventpage.url)
    organizers = event.team.all()

    # Print stuff
    click.echo("OK! That's it. Now I'll copy your event.")

    # Remove #{no} from name:
    name = event.name.split('#')[0].strip()
    number = int(number)
    event_id = event.id

    # Change the name of previous event to {name} #{number-1}
    event.name = "{} #{}".format(name, number-1)
    event.save()

    # Copy event with a name {name} #{number} and new date
    new_event = event
    new_event.pk = None
    new_event.name = "{} #{}".format(name, number)
    new_event.date = date
    new_event.save()

    # Move organizers
    new_event.team = organizers

    # Change the title and url of previous event page
    eventpage.title = "{} #{}".format(name, number-1)
    url = eventpage.url
    if number >= 2:
        new_url = url.replace(str(number-1), str(number))
    else:
        new_url = "{}{}".format(url, number)
    eventpage.save()

    # Copy EventPage object
    new_eventpage = event.eventpage
    new_eventpage.pk = None
    new_eventpage.title = new_event.name
    new_eventpage.url = new_url
    new_eventpage.is_live = False
    new_eventpage.event = new_event
    new_eventpage.save()

    event = Event.objects.get(id=event_id)
    new_eventpage = EventPage.objects.get(event=new_event)

    # Copy all EventPageContent objects
    for obj in event.eventpage.content.all():
        new_content = obj
        new_content.id = None
        new_content.page = new_eventpage
        new_content.save()

        new_content.coaches = obj.coaches.all()
        new_content.sponsors = obj.sponsors.all()

    # Copy all EventPageMenu objects
    for obj in event.eventpage.menu.all():
        new_obj = obj
        new_obj.pk = None
        new_obj.page = new_eventpage
        new_obj.save()

    if number == 2:
        # add link to the previous event in this city
        new_eventpage.menu.create(
            page=new_eventpage,
            title="Last {} event".format(event.city),
            url=previous_url,
            position=int(new_eventpage.menu.latest('position').position)+1
        )
        new_eventpage.save()
    elif number > 2:
        # change link to the previous event
        last_event_link = new_eventpage.menu.latest('position')
        last_event_link.url = previous_url
        last_event_link.save()

    click.echo("Website is ready here: http://djangogirls.org/{0}".format(new_url))
    click.echo("Congrats on yet another event!")
