from core.models import Event


def copy_event(previous_event, event_date):
    """
    Copy event from the previous one. This does the following steps:
    - change name of previous event to {name} #{number}, i.e.
      Django Girls London #1
    - create new event based on previous event
    - copy content and menu from previous event
    """
    number = Event.objects.filter(city=previous_event.city, country=previous_event.country).count()

    previous_event_id = previous_event.pk
    # If event is already Django Girls City #2, remove #2 from it
    if "#" in previous_event.name:
        generic_event_name = previous_event.name.split(" #")[0]
    else:
        generic_event_name = previous_event.name

    previous_event_name = f"{generic_event_name} #{number}"
    event_name = f"{generic_event_name} #{number + 1}"

    # Copy event with a name {name} #{number}, new date and empty stats
    new_event = previous_event
    new_event.pk = None
    new_event.name = event_name
    new_event.date = event_date
    new_event.is_page_live = False
    new_event.attendees_count = None
    new_event.applicants_count = None
    new_event.save()

    # Change url, title and name of previous event to {name} #{number}
    previous_event = Event.objects.get(pk=previous_event_id)
    previous_event.name = previous_event_name
    previous_event.page_title = previous_event_name
    previous_event.page_url = f"{previous_event.page_url}{number}"
    previous_event.save()

    # populate content & menu from the default event
    copy_content_from_previous_event(previous_event, new_event)
    copy_menu_from_previous_event(previous_event, new_event)

    return new_event


def copy_content_from_previous_event(previous_event, new_event):
    """
    Copies page content from the previous event
    """
    previous_event.refresh_from_db()
    for obj in previous_event.content.all():
        new_content = obj
        new_content.id = None
        new_content.event = new_event
        new_content.save()


def copy_menu_from_previous_event(previous_event, new_event):
    """
    Copies page menu from the previous event
    """
    for obj in previous_event.menu.all():
        new_obj = obj
        new_obj.pk = None
        new_obj.event = new_event
        new_obj.save()
