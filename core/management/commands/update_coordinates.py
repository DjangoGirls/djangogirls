# -*- encoding: utf-8 -*-
from __future__ import print_function

from django.core.management.base import BaseCommand

from core.models import Event
from core.utils import get_coordinates_for_city


class Command(BaseCommand):
    help = 'Update coordinates of event cities'

    def handle(self, *args, **options):

        events = Event.objects.all()

        for event in events:
            print(event.city, event.country)
            event.latlng = get_coordinates_for_city(event.city, event.country)
            print(event.latlng)
            event.save()
