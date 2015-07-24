# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import random
import string
import click

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from slacker import Slacker
from slacker import Error as SlackerError

from core.models import *
from core.utils import get_coordinates_for_city, get_approximate_date
from core.default_eventpage_content import get_default_eventpage_data, get_default_menu


slack = Slacker(settings.SLACK_API_KEY)

class Command(BaseCommand):
    help = 'Creates new Django Girls event'

    def get_basic_info(self):
        """
            Here we're asking the user for:
            - city
            - country
            - date
            - url 
            - event_email
            And return all these information.
        """
        click.echo("Hello there! Let's create new Django Girls event! So exciting!")
        click.echo("Let's start with some basics.")
        city = click.prompt(click.style("What is the name of the city?", bold=True, fg='yellow'))
        country = click.prompt(click.style("What is the name of the country?", bold=True, fg='yellow'))
        date = click.prompt(click.style("What is the date of the event? (Format: DD/MM/YYYY or MM/YYYY)", bold=True, fg='yellow'))
        date = get_approximate_date(date)
        while not date:
            date = click.prompt(click.style("Wrong format! Provide a date in format: DD/MM/YYYY or MM/YYYY)", bold=True, fg='yellow'))
            date = get_approximate_date(date)

        url = click.prompt(click.style("What should be the URL of website? djangogirls.org/xxxx", bold=True, fg='yellow'))
        event_mail = click.prompt(click.style("What is the mail adress of the event? xxxx@djangogirls.org", bold=True, fg='yellow'))
        click.echo("Ok, got that! Your new event will happen in {0}, {1} on {2}".format(city, country, date))

        return (city, country, date, url, event_mail)

    def get_main_organizer(self):
        """
            We're asking user for name and address of main organizer, and return
            a list of dictionary.
        """
        team = []
        click.echo("Now let's talk about the team. First the main organizer:")
        main_name = click.prompt(click.style("First and last name", bold=True, fg='yellow'))
        main_email = click.prompt(click.style("E-mail address", bold=True, fg='yellow'))
        try:
            team.append({'first_name': main_name.split(' ')[0], 'last_name': main_name.split(' ')[1], 'email': main_email})
        except IndexError:
            team.append({'first_name': main_name, 'last_name': '', 'email': main_email})
        click.echo(u"All right, the main organizer is {0} ({1})".format(main_name, main_email))

        return team

    def get_team(self, team):
        """
            We're asking user for names and addresss of the rest of the team, and 
            append that to a list we got from get_main_organizer
        """
        add_team = click.confirm(click.style("Do you want to add additional team members?", bold=True, fg='yellow'), default=False)
        i = 1
        while add_team:
            i += 1
            name = click.prompt(click.style("First and last name of #{0} member".format(i), bold=True, fg='yellow'))
            email = click.prompt(click.style("E-mail address of #{0} member".format(i), bold=True, fg='yellow'))
            if len(name) > 0:
                try:
                    team.append({'first_name': name.split(' ')[0], 'last_name': name.split(' ')[1], 'email': email})
                except IndexError:
                    team.append({'first_name': name, 'last_name': '', 'email': email})
                click.echo("All right, the #{0} team member of Django Girls is {1} ({2})".format(i, name, email))
            add_team = click.confirm(click.style("Do you want to add additional team members?", bold=True, fg='yellow'), default=False)

        return team

    def create_users(self, team):
        """
            Create or get User objects based on team list
        """
        members = []
        for member in team:
            if not User.objects.filter(email=member['email']).exists():
                member['password'] = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
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

    def add_default_content(self, page):
        """
            Populate EventPageContent with default layout
        """
        data = get_default_eventpage_data()
        
        i = 0
        for section in data:
            section['page'] = page
            section['position'] = i
            section['content'] = render_to_string(section['template'])
            del section['template']
            EventPageContent.objects.create(**section)
            i += 1


    def add_default_menu(self, page):
        """
            Populate EventPageMenu with default links
        """
        data = get_default_menu()
        
        i = 0
        for link in data:
            link['page'] = page
            link['position'] = i
            EventPageMenu.objects.create(**link)
            i += 1


    def invite_team_to_slack(self, team):
        """
            This uses Slack API to invite organizers to our Slack channel
        """
        for member in team:
            try:
                response = slack.users.invite(member.email, member.first_name)
                click.secho("OK {} invited to Slack".format(member.email), fg='green')
            except SlackerError as e:
                click.secho("!! {} not invited to Slack, because {}".format(member.email, e), fg='red')


    def brag_on_slack_bang(self, city, country, team):
        """
            This is posting a message about Django Girls new event to #general channel on Slack!
        """
        text = ':django_pony: :zap: Woohoo! :tada: New Django Girls alert! Welcome Django Girls {city}, {country}. Congrats {team}!'.format(
            city=city, country=country, team=', '.join(['{} {}'.format(x.first_name, x.last_name) for x in team])
        )
        slack.chat.post_message(
            channel='#general',
            text=text,
            username='Django Girls',
            icon_emoji=':django_heart:'
        )


    def handle(self, *args, **options):
        #Basics
        (city, country, date, url, event_mail) = self.get_basic_info()

        #Main organizer
        main_organizer = self.get_main_organizer()

        #Team
        team = self.get_team(main_organizer)

        #Create users
        click.echo("OK! That's it. Now I'll create your event.")

        members, members_as_list = self.create_users(team)

        #Event and EventPage objects
        name = 'Django Girls '+city
        latlng = get_coordinates_for_city(city, country)
        mail = event_mail+'@djangogirls.org'
        event = Event.objects.create(name=name, city=city, country=country, latlng=latlng,
                                     email=mail, main_organizer=members[0], date=date,
                                     is_on_homepage=False)
        for member in members:
            event.team.add(member)

        page = EventPage.objects.create(event=event, url=url, title=name)

        #Default content
        self.add_default_content(page)
        self.add_default_menu(page)

        click.secho("Website is ready here: http://djangogirls.org/{0}".format(url), fg='green')
        click.echo("")
        click.echo("---------------------------------------------------------------")
        click.echo("")

        self.invite_team_to_slack(members)

        click.echo("")
        click.echo("---------------------------------------------------------------")
        click.echo("")
        
        click.secho("Ok, now follow this:", fg='black', bg='green')
        click.echo("1. Find a photo of a city with CC license on Flickr. Download it.")
        click.echo("2. Go here: http://djangogirls.org/admin/core/event/{0}/".format(event.id))
        click.echo("3. Upload a photo of city, add credits and tick 'is on homepage' checkbox. Save.")
        click.echo("4. Send e-mail with instructions to a team!")
        click.echo("")
        click.echo("---------------------------------------------------------------")
        click.echo("")
        click.secho("This is a ready, filled out mail to sent to organizers:", fg='green')

        click.echo("SUBJECT: Django Girls {} setup".format(event.city))
        click.echo("TO: {}, {}, hello@djangogirls.org".format(
            ', '.join([x.email for x in members]),
            event.email
        ))
        click.echo("BODY:")
        click.echo(render_to_string('emails/setup.txt', {
            'event': event,
            'members': members_as_list,
            'email_password': 'UNDEFINED'
        }))
        
        self.brag_on_slack_bang(city, country, members)
