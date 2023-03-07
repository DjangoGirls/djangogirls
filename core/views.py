import icalendar
from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import TemplateDoesNotExist
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_date_extensions.fields import ApproximateDate

from patreonmanager.models import FundraisingStatus
from story.models import Story

from .models import Event, User


def index(request):
    blogs = Story.objects.filter(is_story=False).order_by("-created")[:3]
    city_count = Event.objects.values("city").distinct().count()
    country_count = Event.objects.values("country").distinct().count()
    future_events = Event.objects.future()
    organizers = User.objects.all().count()
    stories = Story.objects.filter(is_story=True).order_by("-created")[:2]

    return render(
        request,
        "core/index.html",
        {
            "future_events": future_events,
            "stories": stories,
            "blogposts": blogs,
            "patreon_stats": FundraisingStatus.objects.all().first(),  # TODO: This isn't used
            "organizers_count": organizers,
            "cities_count": city_count,
            "country_count": country_count,
        },
    )


def events(request):
    return render(
        request,
        "core/events.html",
        {
            "future_events": Event.objects.future(),
            "past_events": Event.objects.past(),
        },
    )


def events_map(request):
    return render(
        request,
        "core/events_map.html",
        {"events": Event.objects.public().order_by("date"), "mapbox_access_token": settings.MAPBOX_ACCESS_TOKEN},
    )


def resources(request):
    return render(request, "core/resources.html", {})


def event(request, page_url):
    now = timezone.now()
    now_approx = ApproximateDate(year=now.year, month=now.month, day=now.day)

    try:
        event_obj = get_object_or_404(Event, page_url=page_url.lower())
    except Event.MultipleObjectsReturned:
        event_obj = Event.objects.filter(page_url=page_url.lower()).order_by("-date").first()

    user = request.user
    user_is_organizer = user.is_authenticated and event_obj.has_organizer(user)
    is_preview = "preview" in request.GET
    can_preview = user.is_superuser or user_is_organizer or is_preview

    if event_obj.date:
        is_past = event_obj.date <= now_approx
    else:
        is_past = False

    if not (event_obj.is_page_live or can_preview) or event_obj.is_frozen:
        return render(
            request, "applications/event_not_live.html", {"city": event_obj.city, "page_url": page_url, "past": is_past}
        )

    return render(
        request,
        "core/event.html",
        {
            "event": event_obj,
            "menu": event_obj.menu.all(),
            "content": event_obj.content.prefetch_related("coaches", "sponsors").filter(is_public=True),
        },
    )


def events_ical(request):
    events = Event.objects.public().order_by("-date")
    calendar = icalendar.Calendar()
    calendar["summary"] = _("List of Django Girls events around the world")
    for event in events:
        ical_event = event.as_ical()
        if ical_event is None:
            continue  # Skip events with an approximate date
        calendar.add_component(ical_event)

    return HttpResponse(calendar.to_ical(), content_type="text/calendar; charset=UTF-8")


def newsletter(request):
    return render(request, "core/newsletter.html", {})


def faq(request):
    return render(request, "core/faq.html", {})


def foundation(request):
    return render(request, "core/foundation.html", {})


def governing_document(request):
    return render(request, "core/governing_document.html", {})


def contribute(request):
    return render(request, "core/contribute.html", {})


def year_2015(request):
    return render(
        request,
        "core/2015.html",
        {
            "events": Event.objects.public().filter(date__lt="2016-01-01").order_by("date"),
            "mapbox_access_token": settings.MAPBOX_ACCESS_TOKEN,
        },
    )


def year_2016_2017(request):
    return render(
        request,
        "core/2016-2017.html",
        {
            "events": Event.objects.public().filter(date__lt="2017-08-01", date__gte="2016-01-01").order_by("date"),
            "mapbox_access_token": settings.MAPBOX_ACCESS_TOKEN,
        },
    )


def terms_conditions(request):
    return render(request, "core/terms_conditions.html", {})


def privacy_cookies(request):
    return render(request, "core/privacy_cookies.html", {})


# This view's URL is commented out, so avoid coverage hit by commenting out the view also
# def workshop_box(request):
#     return render(request, 'core/workshop_box.html', {})


def server_error(request):
    return HttpResponse(status=500)


def coc(request):
    template_name = "core/coc.html"
    return render(request, template_name)


def coc_legacy(request, lang=None):
    if lang is None:
        lang = "en"
    template_name = f"core/coc/{lang}.html"
    try:
        return render(request, template_name)
    except TemplateDoesNotExist:
        raise Http404(_("No translation for language %(lang)s") % {"lang": lang})


# This view's URL is commented out, so avoid coverage hit by commenting out the view also
# def crowdfunding_donors(request):
#     donor_list = Donor.objects.filter(visible=True).order_by('-amount')
#     return render(request, 'core/crowdfunding_donors.html', {
#         'donor_list': donor_list,
#         'quotes': DONOR_QUOTES,
#     })
