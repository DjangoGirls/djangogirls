from django.shortcuts import render
from django.http import Http404

from core.utils import get_event_page
from core.models import EventPageMenu

def apply(request, city):
    page = get_event_page(city, request.user.is_authenticated(), False)
    if not page:
        raise Http404
    elif type(page) == tuple:
        return render(request, "event_not_live.html", {'city': page[0], 'past': page[1]})

    menu = EventPageMenu.objects.filter(page=page)

    return render(request, 'apply.html', {
        'page': page,
        'menu': menu,
    })
