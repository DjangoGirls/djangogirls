from django.db.models import Sum

from .models import Event, Postmortem


def statistics(request):

    future_events = Event.objects.future()
    past_events = Event.objects.past()
    countries = Event.objects.values('country').distinct()
    attendees = Postmortem.objects.all().aggregate(attendees=Sum('attendees_count'), applicants=Sum('applicants_count'))

    return {
        'past_events_count': past_events.count(),
        'future_events_count': future_events.count(),
        'countries_count': countries.count(),
        'attendees_sum': attendees['attendees'],
        'applicants_sum': attendees['applicants']
    }
