import icalendar

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from .models import Event, EventPage, EventPageMenu, EventPageContent, Story
from .utils import get_event_page


def index(request):

    stories = Story.objects.all().order_by('-created')[:4]

    return render(request, 'index.html', {
        'future_events': Event.objects.future(),
        'past_events': Event.objects.past(),
        'stories': stories,
    })


def events(request):

    return render(request, 'events.html', {
        'future_events': Event.objects.future(),
        'past_events': Event.objects.past(),
    })


def resources(request):
    return render(request, 'resources.html', {})


def organize(request):
    return render(request, 'organize.html', {})


def stories(request):

    return render(request, 'stories.html', {
        'stories': Story.objects.all().order_by('-created'),
    })


def event(request, city):
    page = get_event_page(city, request.user.is_authenticated(), request.GET.has_key('preview'))
    if not page:
        raise Http404
    elif type(page) == tuple:
        return render(request, "event_not_live.html", {'city': page[0], 'past': page[1]})

    menu = EventPageMenu.objects.filter(page=page)
    content = EventPageContent.objects.filter(page=page, is_public=True)

    return render(request, "event.html", {
        'page': page,
        'menu': menu,
        'content': content,
    })


def events_ical(request):
    events = Event.objects.public().order_by('-date')
    calendar = icalendar.Calendar()
    calendar['summary'] = "List of Django Girls events around the world"
    for event in events:
        ical_event = event.as_ical()
        if ical_event is None:
            continue  # Skip events with an approximate date
        calendar.add_component(ical_event)

    return HttpResponse(calendar.to_ical(),
                        content_type='text/calendar; charset=UTF-8')
