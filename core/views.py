import icalendar
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.template import TemplateDoesNotExist
from django.utils import timezone
from django_date_extensions.fields import ApproximateDate

from core.utils import next_deadline
from patreonmanager.models import FundraisingStatus

from .forms import ContactForm
from .models import Event, Story, User


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


def organize(request):
    return render(request, 'core/organize.html', {})


def stories(request):

    return render(request, 'core/stories.html', {
        'stories': Story.objects.filter(is_story=True).order_by('-created'),
    })


def event(request, city):
    now = timezone.now()
    now_approx = ApproximateDate(year=now.year, month=now.month, day=now.day)
    event = get_object_or_404(Event, page_url=city.lower())

    if event.page_url != city:
        return redirect('core:event', city=event.page_url, permanent=True)

    can_show = request.user.is_authenticated() or 'preview' in request.GET
    if not event.is_page_live and not can_show:
        return render(
            request,
            'applications/event_not_live.html',
            {'city': city, 'past': event.date <= now_approx}
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


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            contact_email = form.save()
            if contact_email.sent_successfully:
                messages.add_message(
                    request,
                    messages.INFO,
                    "Thank you for your email. We will be in touch shortly."
                )
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Ooops. We couldn't send your email :( Please try again later"
                )
            return render(request, 'core/contact.html',
                          {'form': ContactForm()})
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})


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


def terms_conditions(request):
    return render(request, 'core/terms_conditions.html', {})


def privacy_cookies(request):
    return render(request, 'core/privacy_cookies.html', {})


def workshop_box(request):
    return render(request, 'core/workshop_box.html', {})

@login_required
def sponsor_request(request):
    return render(request, 'event/sponsor-request.html', {
        'deadline': next_deadline()
    })

def coc(request, lang="en"):
    template_name = "core/coc/{}.html".format(lang)
    try:
        return render(request, template_name)
    except TemplateDoesNotExist:
        raise Http404("No translation for language {}".format(lang))
