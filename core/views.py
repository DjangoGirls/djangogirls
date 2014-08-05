from django.shortcuts import render, redirect
from django.utils import timezone

from .models import *

def index(request):

    events = EventPage.objects.filter(event__is_on_homepage=True).order_by('-event__date')

    return render(request, 'index.html', {
        'events': events,
    })

def event(request, city):
    try:
        if request.user.is_authenticated():
            page = EventPage.objects.get(url=city)
        else:
            page = EventPage.objects.get(url=city, is_live=True)

    except EventPage.DoesNotExist:
        return redirect('index')

    menu = EventPageMenu.objects.filter(page=page)
    content = EventPageContent.objects.filter(page=page)

    return render(request, "event.html", {
        'page': page,
        'menu': menu,
        'content': content,
    })
