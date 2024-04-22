import djclick as click
from django.conf import settings
from django.template.loader import render_to_string

from core.management_utils import brag_on_slack_bang, create_users, get_main_organizer, get_team

from ...command_helpers import gather_event_date_from_prompt
from ...forms import EventForm
from ...utils import get_coordinates_for_city

DELIMITER = "\n-------------------------------------------------------------\n"


def get_basic_info():
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
    city = click.prompt(click.style("What is the name of the city?", bold=True, fg="yellow"))
    country = click.prompt(click.style("What is the name of the country?", bold=True, fg="yellow"))

    date = gather_event_date_from_prompt()

    url = click.prompt(click.style("What should be the URL of website? djangogirls.org/______", bold=True, fg="yellow"))
    event_mail = click.prompt(
        click.style("What is the email prefix of the event? ______@djangogirls.org", bold=True, fg="yellow"),
        default=url,
    )
    click.echo(f"Ok, got that! Your new event will happen in {city}, {country} on {date}")

    return city, country, date, url, event_mail


@click.command()
@click.option("--short", "-s", is_flag=True, help="Shorter version of the setup email to use with a canned email.")
def command(short):
    """Creates new Django Girls event"""
    # Basics
    (city, country, date, url, event_email) = get_basic_info()

    # Main organizer
    main_organizer = get_main_organizer()

    # Team
    team = get_team(main_organizer)

    click.echo("OK! That's it. Now I'll create your event.")

    # Event and EventPage objects
    name = "Django Girls " + city
    latlng = get_coordinates_for_city(city, country)
    email = event_email + "@djangogirls.org"
    form = EventForm(
        {
            "city": city,
            "country": country,
            "date": date,
            "email": email,
            "latlng": latlng,
            "name": name,
            "page_title": name,
            "page_url": url,
        }
    )
    if not form.is_valid():
        click.secho("OOPS! Something went wrong!", fg="red")
        for field, errors in form.errors.items():
            for error in errors:
                click.secho(f"    {field:10} {error}", fg="red")
        return
    event = form.save()

    # Create users
    members = create_users(team, event)
    event.main_organizer = members[0]

    # Add random cover picture
    event.set_random_cover()

    event.save()

    click.secho(f"Website is ready here: http://djangogirls.org/{url}", fg="green")
    click.echo(DELIMITER)

    click.secho("Ok, now follow this:", fg="black", bg="green")
    click.echo("1. Create an email account for the event.")
    click.echo("2. Send e-mail with instructions to a team!")
    click.echo(DELIMITER)
    click.secho("This is a ready, filled out mail to sent to organizers:", fg="green")

    click.echo(f"SUBJECT: Django Girls {event.city} setup")
    click.echo("TO: {}, {}, hello@djangogirls.org".format(", ".join([x.email for x in members]), event.email))
    click.echo("BODY:")

    if short:
        click.echo(
            render_to_string(
                "emails/setup-short.txt",
                {
                    "event": event,
                },
            )
        )
    else:
        click.echo(
            render_to_string("emails/setup.txt", {"event": event, "email_password": "UNDEFINED", "settings": settings})
        )

    brag_on_slack_bang(city, country, members)
