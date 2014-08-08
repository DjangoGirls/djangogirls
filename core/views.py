from datetime import datetime
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import *

def index(request):

    future_events = EventPage.objects.filter(event__is_on_homepage=True, event__date__gte=datetime.now().strftime('%Y-%m-%d')).order_by('event__date')
    past_events = EventPage.objects.filter(event__is_on_homepage=True, event__date__lt=datetime.now().strftime('%Y-%m-%d')).order_by('-event__date')

    return render(request, 'index.html', {
        'future_events': future_events,
        'past_events': past_events,
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
