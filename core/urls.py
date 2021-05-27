from django.urls import re_path

from . import views

app_name = "core"
urlpatterns = [
    # re_path(r'^test-404/$', 'core.views.error404'),
    re_path(r'^events/$', views.events, name='events'),
    re_path(r'^events/map/$', views.events_map, name='events_map'),
    re_path(r'^events/calendar.ics$', views.events_ical, name='icalendar'),
    re_path(r'^resources/$', views.resources, name='resources'),
    re_path(r'^newsletter/$', views.newsletter, name='newsletter'),
    re_path(r'^faq/$', views.faq, name='faq'),
    re_path(r'^foundation/$', views.foundation, name='foundation'),
    re_path(r'^foundation/governing-document/$', views.governing_document,
            name='foundation-governing-document'),
    re_path(r'^contribute/$', views.contribute, name='contribute'),
    re_path(r'^donate/$', views.donate, name='donate'),
    re_path(r'^2015/$', views.year_2015, name='year_2015'),
    re_path(r'^2016-2017/$', views.year_2016_2017, name='year_2016_2017'),
    re_path(r'^terms-conditions/$', views.terms_conditions, name='terms-conditions'),
    re_path(r'^privacy-cookies/$', views.privacy_cookies, name='privacy-cookies'),
    # re_path(r'^workshop-box/$', views.workshop_box, name='workshop-box'),
    re_path(r'^coc/(?:(?P<lang>[a-z-]+)/)?$', views.coc, name='coc'),
    # re_path(r'^crowdfunding-donors/$', views.crowdfunding_donors, name='crowdfunding-donors'),
    re_path(r'^server-error/$', views.server_error, name='server_error'),
    re_path(r'^(?P<city>[\w\d/]+)/$', views.event, name='event'),
    re_path(r'^$', views.index, name='index'),
]
