import calendar
import datetime
from itertools import groupby

import djclick as click
from django.contrib.humanize.templatetags.humanize import apnumber
from django.utils import timezone

from core.models import Event


def generate_html_content(event_list):
    result = []
    for event in event_list:
        city = event.city
        url = event.page_url
        html = f"<a href='https://djangogirls.org/{url}'>{city}</a>"
        result.append(html)
    return result


@click.command()
def command():
    """Generate "Next events" section for the Dispatch."""
    now = timezone.now()
    raw_dispatch_date = click.prompt(
        click.style("What is the date of the previous Dispatch? (Format: YYYY-MM-DD)", bold=True, fg="yellow")
    )

    dispatch_date = datetime.datetime.strptime(raw_dispatch_date, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc)

    # Get the events that happened since the last Dispatch.
    click.echo(click.style("PREVIOUS EVENTS", bold=True))

    previous_events = Event.objects.filter(
        date__gt=dispatch_date.strftime("%Y-%m-%d"), date__lt=now.strftime("%Y-%m-%d")
    )
    result_previous = generate_html_content(previous_events)

    num_events = len(result_previous)

    if result_previous:
        click.echo(
            "{} event{} happened since the last dispatch: ".format(apnumber(num_events), "s" if num_events > 1 else "")
            + ", ".join(result_previous)
            + "."
        )
    else:
        click.echo("No event took place since the last Dispatch.")

    # Get the events that were created since the last Dispatch.

    click.echo(click.style("NEXT EVENTS", bold=True))
    next_events = Event.objects.all().filter(created_at__range=(dispatch_date, now)).order_by("date")

    sorted_event = groupby(next_events, key=lambda event: event.date.month)

    if next_events:
        for month, events in sorted_event:
            month_list = generate_html_content(events)
            click.echo(f"{calendar.month_name[month]}: {', '.join(month_list)}.<br />")
    else:
        click.echo(
            "There's no new event to announce. Don't forget to check our "
            "<a href='https://djangogirls.org/events/'>website</a> to get a "
            "list of our events planned for the next few months."
        )

    # Get the events with open registration.

    click.echo("OPEN REGISTRATION")
    open_events = Event.objects.all().filter(form__open_from__lte=now, form__open_until__gte=now)
    result_open = generate_html_content(open_events)

    if result_open:
        click.echo(f"Registrations are still open for: {', '.join(result_open)}.")
    else:
        click.echo("There's no event with open registration.")
