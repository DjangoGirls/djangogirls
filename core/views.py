import icalendar

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django_date_extensions.fields import ApproximateDate

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


def events_map(request):

    return render(request, 'events_map.html', {
        'events': Event.objects.all().order_by('date'),
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
    now = timezone.now()
    now_approx = ApproximateDate(year=now.year, month=now.month, day=now.day)
    page = get_object_or_404(EventPage, url__iexact=city)

    if page.url != city:
        return redirect('core:event', city=page.url, permanent=True)

    can_show = request.user.is_authenticated() or 'preview' in request.GET
    if not page.is_live and not can_show:
        return render(
            request,
            'event_not_live.html',
            {'city': city, 'past': page.event.date <= now_approx}
        )

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
