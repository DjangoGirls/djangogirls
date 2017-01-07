from django.template.loader import render_to_string

from core.default_eventpage_content import (
    get_default_eventpage_data,
    get_default_menu,
)
from core.models import Event


# TODO: Probably this is not the best place for these two functions.
# Make sure to rethink it once again and refactor core.forms to use
# them, so we do not repeat the code and we preserve ability to create
# Event through Django admin
def _add_default_content(event):
    """Populate EventPageContent with default layout"""
    data = get_default_eventpage_data()

    for i, section in enumerate(data):
        section['position'] = i
        section['content'] = render_to_string(section['template'])
        del section['template']
        event.content.create(**section)


def _add_default_menu(event):
    """Populate EventPageMenu with default links"""
    data = get_default_menu()

    for i, link in enumerate(data):
        link['position'] = i
        event.menu.create(**link)


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
    _add_default_content(event)
    _add_default_menu(event)

    return event
