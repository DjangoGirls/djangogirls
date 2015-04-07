from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^(?P<city>[\w\d/]+)/apply/$',
        'applications.views.apply', name='apply'),
    url(r'^(?P<city>[\w\d/]+)/applications/$',
        'applications.views.applications', name='applications'),
    url(r'^(?P<city>[\w\d/]+)/applications/(?P<app_id>\d+)$',
        'applications.views.application_detail', name='application_detail'),
    url(r'^(?P<city>[\w\d/]+)/applications/change_state/$',
        'applications.views.change_state', name='change_state'),
    url(r'^(?P<city>[\w\d/]+)/communication/$',
        'applications.views.communication', name='communication'),
)
