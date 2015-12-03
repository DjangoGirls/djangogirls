import icalendar
from smtplib import SMTPException

from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django_date_extensions.fields import ApproximateDate

from .models import Event, EventPage, Story, ContactEmail
from .forms import ContactForm


def index(request):

    stories = Story.objects.all().order_by('-created')[:4]

    return render(request, 'index.html', {
        'future_events': Event.objects.select_related('eventpage').future(),
        'past_events': Event.objects.select_related('eventpage').past(),
        'stories': stories,
    })


def events(request):

    return render(request, 'events.html', {
        'future_events': Event.objects.select_related('eventpage').future(),
        'past_events': Event.objects.select_related('eventpage').past(),
    })


def events_map(request):

    return render(request, 'events_map.html', {
        'events': Event.objects.public().order_by('date'),
        'mapbox_map_id': settings.MAPBOX_MAP_ID,
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
    page = get_object_or_404(
        EventPage.objects.select_related('event'),
        url=city.lower()
    )

    if page.url != city:
        return redirect('core:event', city=page.url, permanent=True)

    can_show = request.user.is_authenticated() or 'preview' in request.GET
    if not page.is_live and not can_show:
        return render(
            request,
            'event_not_live.html',
            {'city': city, 'past': page.event.date <= now_approx}
        )

    return render(request, "event.html", {
        'page': page,
        'menu': page.menu.all(),
        'content': page.content.prefetch_related('coaches', 'sponsors').filter(is_public=True),
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
    return render(request, 'newsletter.html', {})


def faq(request):
    return render(request, 'faq.html', {})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            event = form.cleaned_data.get('event')
            if event and event.email:
                to_email = event.email
            else:
                to_email = 'hello@djangogirls.com'

            from_text = "%s %s" % (
                form.cleaned_data['name'], ' - from the djangogirls.org website'
            )

            # Make a note of this email
            ContactEmail.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message'],
                sent_to=to_email,
            )

            try:
                send_mail(
                    from_text,
                    form.cleaned_data['message'],
                    form.cleaned_data['email'],
                    [to_email],
                    fail_silently=False,
                )
            except SMTPException:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Ooops. We couldn't send your email :( Please try again later"
                )
                return render(request, 'contact.html', {'form': form})
            messages.add_message(
                request,
                messages.INFO,
                "Thank you for your email. We will be in touch shortly."
            )
            return render(request, 'contact.html', {'form': ContactForm()})

    else:
        form = ContactForm(initial={'contact_type': ContactForm.CHAPTER})
    return render(request, 'contact.html', {'form': form})


def foundation(request):
    return render(request, 'foundation.html', {})


def governing_document(request):
    return render(request, 'governing_document.html', {})


def contribute(request):
    return render(request, 'contribute.html', {})
