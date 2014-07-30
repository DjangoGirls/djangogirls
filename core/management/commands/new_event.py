# -*- encoding: utf-8 -*-
import random, string, click
from django.core.management.base import BaseCommand, CommandError

from core.models import *

class Command(BaseCommand):
    help = 'Creates new Django Girls event'

    def get_basic_info(self):
        click.echo("Hello there! Let's create new Django Girls event! So exciting!")
        click.echo("Let's start with some basics.")
        city = click.prompt("What is the name of the city?")
        country = click.prompt("What is the name of the country?")
        date = click.prompt("What is the date of the event? (Format: YYYY-MM-DD)")
        url = click.prompt("What should be the URL of website? djangogirls.org/xxxx")
        click.echo(u"Ok, got that! Your new event will happen in {0}, {1} on {2}".format(city, country, date))

        return (city, country, date, url)

    def get_main_organizer(self):
        team = []
        click.echo("Now let's talk about the team. First the main organizer:")
        main_name = click.prompt("First and last name")
        main_email = click.prompt("E-mail address")
        try:
            team.append({'first_name': main_name.split(' ')[0], 'last_name': main_name.split(' ')[1], 'email': main_email})
        except IndexError:
            team.append({'first_name': main_name, 'last_name': '', 'email': main_email})
        click.echo(u"All right, the main organizer is {0} ({1})".format(main_name, main_email))

        return team

    def get_team(self, team):
        add_team = click.prompt("Do you want to add additional team members? y/n")
        i = 1
        while add_team != 'n':
            i += 1
            name = click.prompt("First and last name of #{0} member".format(i))
            email = click.prompt("E-mail address of #{0} member".format(i))
            if len(name) > 0:
                try:
                    team.append({'first_name': name.split(' ')[0], 'last_name': name.split(' ')[1], 'email': email})
                except IndexError:
                    team.append({'first_name': main_name, 'last_name': '', 'email': main_email})
                click.echo(u"All right, the #{0} team member of Django Girls is {1} ({2})".format(i, name, email))
            add_team = click.prompt("Do you want to add additional team members? y/n")

        return team

    def create_users(self, team):
        main_organizer = None
        members = []
        for member in team:
            member['password'] = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
            user = User.objects.create(email=member['email'],
                                        first_name=member['first_name'],
                                        last_name=member['last_name'],
                                        is_active=True,
                                        is_staff=True)
            user.set_password(member['password'])
            user.save()
            user.groups.add(1)

            if not main_organizer:
                main_organizer = user
            members.append(user)
            click.echo(u"{0} - email: {1} password: {2}".format(member['first_name'], member['email'], member['password']))

        return members


    def handle(self, *args, **options):

        #Basics
        (city, country, date, url) = self.get_basic_info()

        #Main organizer
        team = self.get_main_organizer()

        #Team
        team = self.get_team(team)

        #Create users
        click.echo("OK! That's it. Now I'll create your event.")
        click.echo("Here is an access info for team members:")

        members = self.create_users(team)

        #Event and EventPage objects
        name = u'Django Girls '+city
        event = Event.objects.create(name=name, country=country, main_organizer=members[0], date=date)
        for member in members:
            event.team.add(member)

        page = EventPage.objects.create(event=event, url=url, title=name)

        #Default content


        click.echo(u"Website is ready here: http://djangogirls.org/{0}".format(url))
        click.echo("Congrats on yet another event!")
