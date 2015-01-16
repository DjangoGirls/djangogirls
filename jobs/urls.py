from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.jobs, name='jobs'),
    url(r'^details/(?P<id>\d+)$', views.job_details, name='job_details'),
)
