import datetime
from django.core.management import BaseCommand
from django.utils import timezone

from core.models import Event
import click


class Command(BaseCommand):
    help = 'Generate "Next events" section for the Dispatch.'

    def handle(self, *args, **options):
        click.echo(click.style("PREVIOUS EVENTS", bold=True))
        now = timezone.now()
        previous_date = click.prompt(click.style("What is the date of the previous Dispatch? (Format: YYYY-MM-DD)", bold=True, fg='yellow'))
        previous_date = datetime.datetime.strptime(previous_date, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc)
        previous_events = Event.objects.all().filter(created_at__range=(previous_date, now), eventpage__isnull=False)
        num_events = len(previous_events)
        result_previous = []

        for event in previous_events:
            city = event.city
            url = event.eventpage.url
            html = "<a href='https://djangogirls.org/%s'>%s</a>"%(url, city)
            result_previous.append(html)

        print("%s event%s happened since the last dispatch: " %(num_events, "s" if num_events > 1 else "")
              + ", ".join(result_previous) + ".")

        click.echo(click.style("NEXT EVENTS", bold=True))
        '''TODO: print a list of the next events listed by month, with links to eventpage: ex
        June: a
        July: b, c
        '''

        click.echo("OPEN REGISTRATION")
        open_events = Event.objects.all().filter(eventpage__form__open_from__lte=now, eventpage__form__open_until__gte=now)
        result_open = []

        for event in open_events:
            city = event.city
            url = event.eventpage.url
            html = "<a href='https://djangogirls.org/%s'>%s</a>"%(url, city)
            result_open.append(html)

        print("Registrations are still open for: " + ", ".join(result_open) + ".")
