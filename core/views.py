from datetime import datetime
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import *

def index(request):

    stories = Story.objects.all().order_by('-created')[:4]

    return render(request, 'index.html', {
        'future_events': Event.objects.future(),
        'past_events': Event.objects.past(),
        'stories': stories,
    })

def events(request):

    return render(request, 'events.html', {
        'future_events': Event.objects.future(),
        'past_events': Event.objects.past(),
    })

def resources(request):
    return render(request, 'resources.html', {})

def organize(request):
    return render(request, 'organize.html', {})


def event(request, city):
    try:
        if request.user.is_authenticated():
            page = EventPage.objects.get(url=city)
        else:
            page = EventPage.objects.get(url=city, is_live=True)
    except EventPage.DoesNotExist:
        return redirect('core:events')

    menu = EventPageMenu.objects.filter(page=page)
    content = EventPageContent.objects.filter(page=page, is_public=True)

    return render(request, "event.html", {
        'page': page,
        'menu': menu,
        'content': content,
    })
