from django.core.management.base import BaseCommand

from core.models import Event
from core.utils import get_coordinates_for_city


class Command(BaseCommand):
    help = "Update coordinates of event cities"

    def handle(self, *args, **options):

        events = Event.objects.all()

        for event in events:
            self.stdout.write(f"{event.city}, {event.country}")
            event.latlng = get_coordinates_for_city(event.city, event.country)
            self.stdout.write(f"{event.latlng}")
            event.save()
