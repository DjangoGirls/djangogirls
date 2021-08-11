from django.urls import path, re_path

from . import views

app_name = "core"
urlpatterns = [
    # path(r'^test-404/$', 'core.views.error404'),
    path('events/', views.events, name='events'),
    path('events/map/', views.events_map, name='events_map'),
    path('events/calendar.ics', views.events_ical, name='icalendar'),
    path('resources/', views.resources, name='resources'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('faq/', views.faq, name='faq'),
    path('foundation/', views.foundation, name='foundation'),
    path('foundation/governing-document/', views.governing_document, name='foundation-governing-document'),
    path('contribute/', views.contribute, name='contribute'),
    path('2015/', views.year_2015, name='year_2015'),
    path('2016-2017/', views.year_2016_2017, name='year_2016_2017'),
    path('terms-conditions/', views.terms_conditions, name='terms-conditions'),
    path('privacy-cookies/', views.privacy_cookies, name='privacy-cookies'),
    # path(r'^workshop-box/$', views.workshop_box, name='workshop-box'),
    re_path(r'^coc/(?:(?P<lang>[a-z-]+)/)?$', views.coc, name='coc'),
    # path(r'^crowdfunding-donors/$', views.crowdfunding_donors, name='crowdfunding-donors'),
    path('server-error/', views.server_error, name='server_error'),
    path('<slug:page_url>/', views.event, name='event'),
    path('', views.index, name='index'),
]
