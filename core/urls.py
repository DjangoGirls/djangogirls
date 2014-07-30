from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^(?P<city>[\w\d]+)', 'core.views.event', name='event'),
    url(r'^$', views.index, name='index'),
)
