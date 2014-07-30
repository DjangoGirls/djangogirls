from django.shortcuts import render, redirect
from django.utils import timezone

from .models import *

def index(request):

    upcoming_events = EventPage.objects.filter(is_live=True, event__date__gt=timezone.now()).order_by('-event__date')
    past_events = EventPage.objects.filter(is_live=True, event__date__lt=timezone.now()).order_by('-event__date')

    return render(request, 'index.html', {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    })

def event(request, city):
    try:
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
