from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
#    url(r'^test-404/$', 'core.views.error404'),
    url(r'^events/$', views.events, name='events'),
    url(r'^events/map/$', views.events_map, name='events_map'),
    url(r'^events/calendar.ics$', views.events_ical, name='icalendar'),
    url(r'^resources/$', views.resources, name='resources'),
    url(r'^organize/$', views.organize, name='organize'),
    url(r'^story/$', views.stories, name='stories'),
    url(r'^newsletter/$', views.newsletter, name='newsletter'),

    url(r'^(?P<city>[\w\d]+)/$', 'core.views.event', name='event'),
    url(r'^$', views.index, name='index'),
)
