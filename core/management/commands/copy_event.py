# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import click
from datetime import datetime

from django.core.management.base import BaseCommand
from django_date_extensions.fields import ApproximateDate

from core.models import *


class Command(BaseCommand):
    help = 'Duplicates Django Girls event with a new date'

    def prepare_date(self, date_str):
        try:
            date_obj = datetime.strptime(date_str, '%d/%m/%Y')
            return ApproximateDate(year=date_obj.year, month=date_obj.month, day=date_obj.day)
        except ValueError:
            try:
                date_obj = datetime.strptime(date_str, '%m/%Y')
                return ApproximateDate(year=date_obj.year, month=date_obj.month)
            except ValueError:
                return False

        return False

    def get_event(self, id_str):
        try:
            return Event.objects.get(id=int(id_str))
        except (ValueError, Event.DoesNotExist):
            return False

    def gather_information(self):
        click.echo("Hello there sunshine! We're gonna copy an event website now.")

        event = self.get_event(click.prompt("First, give me the ID of the Event object we're gonna copy. Don't mix it up with EventPage object. If there is more than one event in this city already, give me ID of the latest one"))
        while not event:
            event = self.get_event(click.prompt("Wrong ID! Try again"))

        number = click.prompt("What is the number of the event in this city? If this is a second event, write 2. If third, then 3. You got it")

        date = self.prepare_date(click.prompt("What is the date of this new event? (Format: DD/MM/YYYY or MM/YYYY)"))
        while not date:
            date = self.prepare_date(click.prompt("Wrong format! Provide a date in format: DD/MM/YYYY or MM/YYYY)"))

        return (event, number, date)

    def handle(self, *args, **options):

        # Gather data
        (event, number, date) = self.gather_information()
        eventpage = event.eventpage
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
        new_event.id = None
        new_event.name = "{} #{}".format(name, number)
        new_event.date = date
        new_event.save()

        # Move organizers
        new_event = Event.objects.get(id=new_event.id)
        for organizer in organizers:
            new_event.team.add(organizer)
            new_event.save()

        # Change the title and url of previous event page
        eventpage.title = "{} #{}".format(name, number-1)
        url = eventpage.url
        eventpage.url = "{}{}".format(url, number-1)
        eventpage.save()

        # Copy EventPage object
        new_eventpage = event.eventpage
        new_eventpage.id = None
        new_eventpage.pk = None
        new_eventpage.title = new_event.name
        new_eventpage.url = url
        new_eventpage.is_live = False
        new_eventpage.event = new_event
        new_eventpage.save()

        event = Event.objects.get(id=event_id)
        eventpage = event.eventpage
        new_eventpage = EventPage.objects.get(event=new_event)

        # Copy all EventPageContent objects
        for obj in event.eventpage.eventpagecontent_set.all():
            obj_id = obj.id
            new_content = obj
            new_content.id = None
            new_content.pk = None
            new_content.page = new_eventpage
            new_content.save()

            obj = EventPageContent.objects.get(id=obj_id)
            
            new_content.coaches.add(*obj.coaches.all())
            new_content.sponsors.add(*obj.sponsors.all())

        # Copy all EventPageMenu objects
        for obj in event.eventpage.eventpagemenu_set.all():
            obj.id = None
            obj.pk = None
            obj.page = new_eventpage
            obj.save()

        click.echo("Website is ready here: http://djangogirls.org/{0}".format(url))
        click.echo("Congrats on yet another event!")
