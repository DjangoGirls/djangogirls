from django.db.models import Sum

from globalpartners.models import GlobalPartner

from .models import Event, User


def statistics(request):
    future_events = Event.objects.future()
    past_events = Event.objects.past()
    countries = Event.objects.values("country").distinct()
    attendees = Event.objects.all().aggregate(attendees=Sum("attendees_count"), applicants=Sum("applicants_count"))
    organizers = User.objects.filter(is_active=True)
    global_partners = GlobalPartner.objects.filter(is_displayed=True)
    bronze = global_partners.filter(sponsor_level_annual=500)
    diamond = global_partners.filter(sponsor_level_annual=10000)
    gold = global_partners.filter(sponsor_level_annual=2500)
    platinum = global_partners.filter(sponsor_level_annual=5000)
    silver = global_partners.filter(sponsor_level_annual=1000)
    bronze = global_partners.filter(sponsor_level_annual=500)

    return {
        "past_events_count": past_events.count(),
        "future_events_count": future_events.count(),
        "all_events_count": past_events.count() + future_events.count(),
        "countries_count": countries.count(),
        "attendees_sum": attendees["attendees"],
        "applicants_sum": attendees["applicants"],
        "organizers_count": organizers.count(),
        "bronze": bronze,
        "diamond": diamond,
        "gold": gold,
        "platinum": platinum,
        "silver": silver,
        "bronze": bronze,
    }
