from django.template.loader import render_to_string

from core.default_eventpage_content import (
    get_default_eventpage_data,
    get_default_menu,
)
from core.models import Event


def create_event_from_event_application(event_application):
    """ Creates event based on the data from the object.
        If the event has previous_event - we are copying data from the
        existing old event for the given city.
    """
    name = 'Django Girls {}'.format(event_application.city)
    email = '{}@djangogirls.org'.format(event_application.website_slug)

    # TODO: take care of copying the event

    event = Event.objects.create(
        date=event_application.date,
        city=event_application.city,
        country=event_application.country,
        latlng=event_application.latlng,
        page_url=event_application.website_slug,
        name=name,
        page_title=name,
        email=email,
    )

    # populate content & menu from the default event
    event.add_default_content()
    event.add_default_menu()

    return event
