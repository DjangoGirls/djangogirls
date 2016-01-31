from django.db.models import Sum

from .models import Event, Postmortem
from jobs.models import Meetup


def statistics(request):
    future_events = Event.objects.future()
    past_events = Event.objects.past()
    countries = Event.objects.values('country').distinct()
    attendees = Postmortem.objects.all().aggregate(attendees=Sum('attendees_count'), applicants=Sum('applicants_count'))
    meetup_count = Meetup.visible_objects.count()

    return {
        'past_events_count': past_events.count(),
        'future_events_count': future_events.count(),
        'all_events_count': past_events.count() + future_events.count(),
        'countries_count': countries.count(),
        'attendees_sum': attendees['attendees'],
        'applicants_sum': attendees['applicants'],
        'meetup_count': meetup_count
    }
