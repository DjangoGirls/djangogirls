import calendar
import datetime
from itertools import groupby
from django.core.management import BaseCommand
from django.utils import timezone

from core.models import Event
import click


class Command(BaseCommand):
    help = 'Generate "Next events" section for the Dispatch.'

    def handle(self, *args, **options):
        now = timezone.now()
        raw_dispatch_date = click.prompt(click.style("What is the date of the previous Dispatch? (Format: YYYY-MM-DD)", bold=True, fg='yellow'))
        dispatch_date = datetime.datetime.strptime(raw_dispatch_date, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc)

        click.echo(click.style("PREVIOUS EVENTS", bold=True))

        def done_since_last_dispatch(event):
            # Sadly, ApproximateDate won't let us do that in SQL
            approx_date = event.date
            if not approx_date.day:
                return False  # No specific date, so ignore it
            date = datetime.datetime(approx_date.year, approx_date.month, approx_date.day, tzinfo=datetime.timezone.utc)
            return dispatch_date < date < now

        previous_events = filter(done_since_last_dispatch, Event.objects.all().filter(eventpage__isnull=False))
        result_previous = []

        for event in previous_events:
            city = event.city
            url = event.eventpage.url
            html = "<a href='https://djangogirls.org/%s'>%s</a>"%(url, city)
            result_previous.append(html)

        num_events = len(result_previous)

        if not result_previous:
            print("No event took place since the last Dispatch.")
        else:
            print("%s event%s happened since the last dispatch: " %(num_events, "s" if num_events > 1 else "")
              + ", ".join(result_previous) + ".")

        click.echo(click.style("NEXT EVENTS", bold=True))
        next_events = Event.objects.all().filter(created_at__range=(dispatch_date, now), eventpage__isnull=False)

        sorted_event = groupby(next_events, key=lambda event: event.date.month)

        if not next_events:
            print("There's no new event to announce. Don't forget to check our <a href='https://djangogirls.org/events/'>website</a> to get a list of our events planned for the next few months.")
        else:
            for month, events in sorted_event:
                month_list = []
                for event in events:
                    city = event.city
                    url = event.eventpage.url
                    html = "<a href='https://djangogirls.org/%s'>%s</a>" % (url, city)
                    month_list.append(html)
                print(calendar.month_name[month] + ": " + ", ".join(month_list) + ".")



        click.echo("OPEN REGISTRATION")
        open_events = Event.objects.all().filter(eventpage__form__open_from__lte=now, eventpage__form__open_until__gte=now, eventpage__isnull=False)
        result_open = []

        for event in open_events:
            city = event.city
            url = event.eventpage.url
            html = "<a href='https://djangogirls.org/%s'>%s</a>"%(url, city)
            result_open.append(html)

        if not result_open:
            print("There's no event with open registration.")
        else:
            print("Registrations are still open for: " + ", ".join(result_open) + ".")
