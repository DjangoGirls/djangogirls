from datetime import datetime

from django.db.models import Sum

from .models import EventPage, Event, Postmortem


def statistics(request):

    future_events = EventPage.objects.filter(event__is_on_homepage=True, event__date__gte=datetime.now().strftime('%Y-%m-%d')).order_by('event__date')
    past_events = EventPage.objects.filter(event__is_on_homepage=True, event__date__lt=datetime.now().strftime('%Y-%m-%d')).order_by('-event__date')
    countries = Event.objects.values('country').distinct()
    attendees = Postmortem.objects.all().aggregate(attendees=Sum('attendees_count'), applicants=Sum('applicants_count'))

    return {
        'past_events_count': past_events.count(),
        'future_events_count': future_events.count(),
        'countries_count': countries.count(),
        'attendees_sum': attendees['attendees'],
        'applicants_sum': attendees['applicants']
    }
