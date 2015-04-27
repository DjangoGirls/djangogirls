from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.main, name='main'),
    url(r'^jobs$', views.jobs, name='jobs'),
    url(r'^meetups$', views.meetups, name='meetups'),
    url(r'^job/(?P<id>\d+)$', views.job_details, name='job_details'),
    url(r'^confirm_submission$', views.confirm_submission, name='confirm_submission'),
    url(r'^meetup/(?P<id>\d+)$', views.meetup_details, name='meetup_details'),
    url(r'^job/new$', views.create_job, name='job_new'),
    url(r'^meetup/new$', views.create_meetup, name='meetup_new'),
)
