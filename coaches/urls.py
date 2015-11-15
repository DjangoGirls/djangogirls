from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^(?P<city>[\w\d/]+)/register_as_coach/$',
        'coaches.views.register', name='register_as_coach'),
    url(r'^(?P<city>[\w\d/]+)/coach_applications/(?P<coach_app_id>\d+)/$',
        'coaches.views.coach_application_detail', name='coach_detail'),
    url(r'^(?P<city>[\w\d/]+)/coach_applications/$',
        'coaches.views.coach_applications', name='coach_applications'),
    url(r'^(?P<city>[\w\d/]+)/coach_applications/change_state/$',
        'coaches.views.change_state', name='change_coach_state'),
    url(r'^(?P<city>[\w\d/]+)/coach_applications/download/$',
        'coaches.views.applications_csv', name='coach_applications_csv'),
    url(r'^(?P<city>[\w\d/]+)/coach_communication/$',
        'coaches.views.communication', name='coach_communication'),
    url(r'^(?P<city>[\w\d/]+)/coach_communication/compose/(?P<email_id>\d+)$',
        'coaches.views.compose_email', name='compose_coach_email'),
    url(r'^(?P<city>[\w\d/]+)/coach_communication/compose/$',
        'coaches.views.compose_email', name='compose_coach_email'),
)
