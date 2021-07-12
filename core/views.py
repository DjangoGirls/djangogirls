from datetime import date

import icalendar
from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.template.exceptions import TemplateDoesNotExist

from patreonmanager.models import FundraisingStatus

from .models import Event, User
from story.models import Story
from sponsor.models import Donor
from .quotes import DONOR_QUOTES


def index(request):

    return render(request, 'core/index.html', {
        'future_events': Event.objects.future(),
        'stories': Story.objects.filter(is_story=True).order_by('-created')[:2],
        'blogposts': Story.objects.filter(is_story=False).order_by('-created')[:3],
        'patreon_stats': FundraisingStatus.objects.all().first(),
        'organizers_count': User.objects.all().count(),
        'cities_count': Event.objects.values('city').distinct().count(),
        'country_count': Event.objects.values('country').distinct().count(),
    })


def events(request):

    return render(request, 'core/events.html', {
        'future_events': Event.objects.future(),
        'past_events': Event.objects.past(),
    })


def events_map(request):

    return render(request, 'core/events_map.html', {
        'events': Event.objects.public().order_by('date'),
        'mapbox_map_id': settings.MAPBOX_MAP_ID,
    })


def resources(request):
    return render(request, 'core/resources.html', {})


def event(request, city):
    now_approx = date.today()
    event = get_object_or_404(Event, page_url=city.lower())

    if event.page_url != city:
        return redirect('core:event', city=event.page_url, permanent=True)

    user = request.user
    user_is_organizer = user.is_authenticated and event.has_organizer(user)
    is_preview = 'preview' in request.GET
    previewable = user.is_superuser or user_is_organizer or is_preview

    if not (event.is_page_live or previewable):
        return render(
            request,
            'applications/event_not_live.html',
            {'city': city, 'past': False}
        )

    return render(request, "core/event.html", {
        'event': event,
        'menu': event.menu.all(),
        'content': event.content.prefetch_related('coaches', 'sponsors').filter(is_public=True),
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


def newsletter(request):
    return render(request, 'core/newsletter.html', {})


def faq(request):
    return render(request, 'core/faq.html', {})


def foundation(request):
    return render(request, 'core/foundation.html', {})


def governing_document(request):
    return render(request, 'core/governing_document.html', {})


def contribute(request):
    return render(request, 'core/contribute.html', {})


def donate(request):
    return render(request, 'core/donate.html', {
        'patreon_stats': FundraisingStatus.objects.all().first(),
    })


def year_2015(request):
    return render(request, 'core/2015.html', {
        'events': Event.objects.public().filter(date__lt='2016-01-01').order_by('date'),
        'mapbox_map_id': settings.MAPBOX_MAP_ID,
    })


def year_2016_2017(request):
    return render(request, 'core/2016-2017.html', {
        'events_2015': Event.objects.public().filter(date__lt='2016-01-01').order_by('date'),
        'events_20162017': Event.objects.public().filter(date__lt='2017-08-01', date__gte='2016-01-01').order_by('date'),
        'mapbox_map_id': settings.MAPBOX_MAP_ID,
    })


def terms_conditions(request):
    return render(request, 'core/terms_conditions.html', {})


def privacy_cookies(request):
    return render(request, 'core/privacy_cookies.html', {})


def workshop_box(request):
    return render(request, 'core/workshop_box.html', {})


def server_error(request):
    return HttpResponse(status=500)


def coc(request, lang=None):
    if lang is None:
        lang = 'en'
    template_name = "core/coc/{}.html".format(lang)
    try:
        return render(request, template_name)
    except TemplateDoesNotExist:
        raise Http404("No translation for language {}".format(lang))


def crowdfunding_donors(request):
    donor_list = Donor.objects.filter(visible=True).order_by('-amount')
    return render(request, 'core/crowdfunding_donors.html', {
        'donor_list': donor_list,
        'quotes': DONOR_QUOTES,
    })
