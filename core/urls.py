from django.conf.urls import url

from . import views

app_name = "core"
urlpatterns = [
    # url(r'^test-404/$', 'core.views.error404'),
    url(r'^events/$', views.events, name='events'),
    url(r'^events/map/$', views.events_map, name='events_map'),
    url(r'^events/calendar.ics$', views.events_ical, name='icalendar'),
    url(r'^resources/$', views.resources, name='resources'),
    url(r'^newsletter/$', views.newsletter, name='newsletter'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^foundation/$', views.foundation, name='foundation'),
    url(r'^foundation/governing-document/$', views.governing_document,
        name='foundation-governing-document'),
    url(r'^contribute/$', views.contribute, name='contribute'),
    url(r'^donate/$', views.donate, name='donate'),
    url(r'^2015/$', views.year_2015, name='year_2015'),
    url(r'^2016-2017/$', views.year_2016_2017, name='year_2016_2017'),
    url(r'^terms-conditions/$', views.terms_conditions, name='terms-conditions'),
    url(r'^privacy-cookies/$', views.privacy_cookies, name='privacy-cookies'),
    # url(r'^workshop-box/$', views.workshop_box, name='workshop-box'),
    url(r'^coc/(?:(?P<lang>[a-z-]+)/)?$', views.coc, name='coc'),
    # url(r'^crowdfunding-donors/$', views.crowdfunding_donors, name='crowdfunding-donors'),
    url(r'^server-error/$', views.server_error, name='server_error'),
    url(r'^(?P<city>[\w\d/]+)/$', views.event, name='event'),
    url(r'^$', views.index, name='index'),
]
