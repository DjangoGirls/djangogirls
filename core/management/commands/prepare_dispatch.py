from django.core.management import BaseCommand
from django.utils import timezone

from core.models import Event


class Command(BaseCommand):
    help = 'Generate "Next events" section for the Dispatch.'

    def handle(self, *args, **options):
        print("PREVIOUS EVENTS")
        #TODO: print a list of previous events since the last dispatch with links to eventpage. Ex: Nine events happended since the last dispatch: a, b, c...

        print("NEXT EVENTS")
        '''TODO: print a list of the next events listed by month, with links to eventpage: ex
        June: a
        July: b, c
        '''

        print("OPEN REGISTRATION")
        now = timezone.now()
        open_events = Event.objects.all().filter(eventpage__form__open_from__lte=now, eventpage__form__open_until__gte=now)
        result = []

        for event in open_events:
            city = event.city
            url = event.eventpage.url
            html = "<a href='https://djangogirls.org/%s'>%s</a>"%(url, city)
            result.append(html)

        print("Registrations are still open for: " + ", ".join(result))
