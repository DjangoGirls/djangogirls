from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^(?P<city>[\w\d/]+)/apply/$', 'applications.views.apply', name='apply'),
)
