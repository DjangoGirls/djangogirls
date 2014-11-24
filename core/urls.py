from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^events/$', views.events, name='events'),
    url(r'^resources/$', views.resources, name='resources'),
    url(r'^organize/$', views.organize, name='organize'),
    url(r'^story/$', views.stories, name='stories'),
    url(r'^calendar/$', views.events_ical, name='icalendar'),

    url(r'^(?P<city>[\w\d/]+)$', 'core.views.event', name='event'),
    url(r'^$', views.index, name='index'),
)
