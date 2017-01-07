from django.conf.urls import url

from applications import views

urlpatterns = [
    url(r'^(?P<city>[\w\d/]+)/apply/$', views.apply, name='apply'),
    url(r'^(?P<city>[\w\d/]+)/applications/$',
        views.application_list, name='applications'),
    url(r'^(?P<city>[\w\d/]+)/applications/(?P<app_number>\d+)$',
        views.application_detail, name='application_detail'),
    url(r'^(?P<city>[\w\d/]+)/applications/change_state/$',
        views.change_state, name='change_state'),
    url(r'^(?P<city>[\w\d/]+)/applications/change_rsvp/$',
        views.change_rsvp, name='change_rsvp'),
    url(r'^(?P<city>[\w\d/]+)/applications/download/$',
        views.applications_csv, name='applications_csv'),
    url(r'^(?P<city>[\w\d/]+)/communication/$',
        views.communication, name='communication'),
    url(r'^(?P<city>[\w\d/]+)/communication/compose/$',
        views.compose_email, name='compose_email'),
    url(r'^(?P<city>[\w\d/]+)/communication/compose/(?P<email_id>\d+)$',
        views.compose_email, name='compose_email'),
    url(r'^(?P<city>[\w\d/]+)/rsvp/(?P<code>[\w\d/]+)$',
        views.rsvp, name='rsvp'),
]
