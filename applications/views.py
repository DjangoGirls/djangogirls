from django.shortcuts import render, redirect
from django.http import Http404

from core.utils import get_event_page
from core.models import EventPageMenu
from .models import Form

def apply(request, city):
    page = get_event_page(city, request.user.is_authenticated(), False)
    if not page:
        raise Http404
    elif type(page) == tuple:
        return render(request, "event_not_live.html", {'city': page[0], 'past': page[1]})

    try:
        form = Form.objects.get(page=page)
    except Form.DoesNotExist:
        return redirect('core:event', city)

    menu = EventPageMenu.objects.filter(page=page)

    return render(request, 'apply.html', {
        'page': page,
        'menu': menu,
        'form': form,
    })
