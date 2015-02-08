from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.jobs, name='jobs'),
    url(r'^job/(?P<id>\d+)$', views.job_details, name='job_details'),
    url(r'^meetup/(?P<id>\d+)$', views.meetup_details, name='meetup_details'),
    url(r'^job/new$', views.JobCreate.as_view(), name='job_new'),
)
