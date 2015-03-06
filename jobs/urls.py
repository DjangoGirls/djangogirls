from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^jobs$', views.jobs, name='jobs'),
    url(r'^meetups$', views.meetups, name='meetups'),
    url(r'^job/(?P<id>\d+)$', views.job_details, name='job_details'),
    url(r'^meetup/(?P<id>\d+)$', views.meetup_details, name='meetup_details'),
    url(r'^job/new$', views.JobCreate.as_view(), name='job_new'),
    url(r'^meetup/new$', views.MeetupCreate.as_view(), name='meetup_new'),
)
