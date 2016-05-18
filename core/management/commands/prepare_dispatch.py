from django.core.management import BaseCommand
from django.utils import timezone

from core.models import Event


class Command(BaseCommand):
    help = 'Generate "Next events" section for the Dispatch.'

    def handle(self, *args, **options):
        now = timezone.now()
        open_events = Event.objects.all().filter(eventpage__form__open_from__lte=now, eventpage__form__open_until__gte=now)
        result = []

        for event in open_events:
            city = event.city
            url = event.eventpage.url
            html = "<a href='https://djangogirls.org/%s'>%s</a>"%(url, city)
            result.append(html)

        print(", ".join(result))
