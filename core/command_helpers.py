import djclick as click

from core.utils import get_approximate_date


def gather_event_date_from_prompt():
    date = None
    while date is None:
        date_str = click.prompt(
            click.style("What is the date of the event? (Format: DD/MM/YYYY or MM/YYYY)", bold=True, fg="yellow")
        )
        date = get_approximate_date(date_str)
        if date is None:
            click.secho("Wrong format! Try again :)", bold=True, fg="red")

    return date
