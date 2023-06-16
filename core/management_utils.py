import djclick as click
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from core.forms import AddOrganizerForm
from core.slack_client import post_message_to_slack

# "Get organizers info" functions used in 'new_event' and 'copy_event' management commands.


def get_main_organizer():
    """
    We're asking user for name and address of main organizer, and return
    a list of dictionary.
    """
    team = []
    click.echo(_("Let's talk about the team. First the main organizer:"))
    main_name = click.prompt(click.style("First and last name", bold=True, fg="yellow"))
    main_email = click.prompt(click.style("E-mail address", bold=True, fg="yellow"))

    team.append({"name": main_name, "email": main_email})

    click.echo(f"All right, the main organizer is {main_name} ({main_email})")

    return team


def get_team(team):
    """
    We're asking user for names and address of the rest of the team,
    and append that to a list we got from get_main_organizer
    """
    add_team = click.confirm(
        click.style("Do you want to add additional team members?", bold=True, fg="yellow"), default=False
    )
    i = 1
    while add_team:
        i += 1
        name = click.prompt(click.style(f"First and last name of #{i} member", bold=True, fg="yellow"))
        email = click.prompt(click.style(f"E-mail address of #{i} member", bold=True, fg="yellow"))
        if len(name) > 0:
            team.append({"name": name, "email": email})
            click.echo(f"All right, the #{i} team member of Django Girls is {name} ({email})")
        add_team = click.confirm(
            click.style("Do you want to add additional team members?", bold=True, fg="yellow"), default=False
        )

    return team


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


def brag_on_slack_bang(city, country, team):
    """
    This is posting a message about Django Girls new event to #general channel on Slack!
    """
    if settings.ENABLE_SLACK_NOTIFICATIONS:
        text = (
            f":django_pony: :zap: Woohoo! :tada: New Django Girls alert! "
            f"Welcome Django Girls {city}, {country}. "
            f"Congrats {', '.join(['{} {}'.format(x.first_name, x.last_name) for x in team])}!"
        )

        post_message_to_slack("#general", text)
