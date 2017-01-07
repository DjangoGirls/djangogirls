from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^test-404/$', 'core.views.error404'),
    url(r'^events/$', views.events, name='events'),
    url(r'^events/map/$', views.events_map, name='events_map'),
    url(r'^events/calendar.ics$', views.events_ical, name='icalendar'),
    url(r'^resources/$', views.resources, name='resources'),
    url(r'^organize/$', views.organize, name='organize'),
    url(r'^story/$', views.stories, name='stories'),
    url(r'^newsletter/$', views.newsletter, name='newsletter'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^foundation/$', views.foundation, name='foundation'),
    url(r'^foundation/governing-document/$', views.governing_document,
        name='foundation-governing-document'),
    url(r'^contribute/$', views.contribute, name='contribute'),
    url(r'^donate/$', views.donate, name='donate'),
    url(r'^2015/$', views.year_2015, name='year_2015'),
    url(r'^terms-conditions/$', views.terms_conditions, name='terms-conditions'),
    url(r'^privacy-cookies/$', views.privacy_cookies, name='privacy-cookies'),
    url(r'^workshop-box/$', views.workshop_box, name='workshop-box'),
    url(r'^coc/(?:(?P<lang>[a-z-]+)/)?$', views.coc, name='coc'),
    url(r'^translators/invite/$', views.translator_invite, name='translator-invite'),
    url(r'^translators/YAY/$', views.translator_invite_success, name='translator-invite-success'),

    url(r'^(?P<city>[\w\d/]+)/$', views.event, name='event'),
    url(r'^sponsor-request/$', views.sponsor_request, name='sponsor-request'),
    url(r'^$', views.index, name='index'),
]
