# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import djclick as click
import random
from slacker import Error as SlackerError
import string


from core.models import User, Event
from core.slack_client import user_invite


help = 'Creates new Django Girls organizer'


def get_organizer_data():
    """
        Returns a dictionary with first_name, last_name and email
    """
    main_name = click.prompt(click.style(
        "First and last name", bold=True, fg='yellow'))
    main_email = click.prompt(click.style(
        "E-mail address", bold=True, fg='yellow'))
    try:
        data = {'first_name': main_name.split(' ')[0],
                'last_name': main_name.split(' ')[1],
                'email': main_email}
    except IndexError:
        data = {'first_name': main_name,
                'last_name': '', 'email': main_email}

    return data


def create_users(team):
    """
        Create or get User objects based on team list
    """
    members = []
    for member in team:
        if not User.objects.filter(email=member['email']).exists():
            member['password'] = ''.join(random.choice(
                string.ascii_lowercase + string.digits) for _ in range(8))
            user = User.objects.create(email=member['email'],
                                       first_name=member['first_name'],
                                       last_name=member['last_name'],
                                       is_active=True,
                                       is_staff=True)
            user.set_password(member['password'])
            user.save()
            user.groups.add(1)
        else:
            user = User.objects.get(email=member['email'])
        members.append(user)
    return members, team


def invite_team_to_slack(team):
    """
        This uses Slack API to invite organizers to our Slack channel
    """
    for member in team:
        try:
            user_invite(member.email, member.first_name)
            click.secho("OK {} invited to Slack".format(
                member.email), fg='green')
        except SlackerError as e:
            click.secho("!! {} not invited to Slack, because {}".format(
                member.email, e), fg='red')


@click.command()
def command():
    event_id = click.prompt(
        click.style(
            "What's the event ID? NOT the event page ID. We want EVENT ID here",
            bold=True, fg='yellow'))
    event = Event.objects.get(id=event_id)
    click.echo("Ok, we're adding to an event in {}, {}".format(
        event.city, event.country))

    team = [get_organizer_data()]

    while click.confirm(
        click.style("Do you want to add additional team members?",
                    bold=True, fg='yellow'), default=False):
        team.append(get_organizer_data())

    click.echo("OK! That's it. Now I'll add your organizers.")

    members, members_as_list = create_users(team)

    for member in members:
        event.team.add(member)

    event.save()

    for member in members_as_list:
        if 'password' in member:
            click.echo("{} - email: {} password {}".format(
                member['first_name'], member['email'], member['password']))
        else:
            click.echo(
                "{} - email: {} already has account".format(
                    member['first_name'], member['email']))

    click.echo("")
    click.echo(
        "---------------------------------------------------------------")
    click.echo("")

    invite_team_to_slack(members)

    click.echo("")
    click.echo(
        "---------------------------------------------------------------")
    click.echo("")

    click.echo("You still need to invite people to Google Group!")
