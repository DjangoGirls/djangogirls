import djclick as click

from core.forms import AddOrganizerForm
from core.models import Event

DELIMITER = "\n-------------------------------------------------------------\n"


def get_organizer_data():
    """
    Returns a dictionary with first_name, last_name and email
    """
    main_name = click.prompt(click.style("First and last name", bold=True, fg="yellow"))
    main_email = click.prompt(click.style("E-mail address", bold=True, fg="yellow"))

    data = {"name": main_name, "email": main_email}

    return data


def create_users(team, event):
    """
    Create or get User objects based on team list
    """
    members = []
    for member in team:
        member["event"] = event.pk
        form = AddOrganizerForm(member)
        user = form.save()
        members.append(user)
    return members


@click.command()
def command():
    """Creates new Django Girls organizer"""
    event_id = click.prompt(
        click.style("What's the event ID? NOT the event page ID. We want EVENT ID here", bold=True, fg="yellow")
    )
    event = Event.objects.get(id=event_id)
    click.echo(f"Ok, we're adding to an event in {event.city}, {event.country}")
    team = [get_organizer_data()]

    while click.confirm(
        click.style("Do you want to add additional team members?", bold=True, fg="yellow"), default=False
    ):
        team.append(get_organizer_data())

    click.echo("OK! That's it. Now I'll add your organizers.")

    members = create_users(team, event)

    for member in members:
        click.echo(f"User {member.email} has been added and notified")

    click.echo(DELIMITER)

    click.echo("You still need to invite people to Google Group!")
