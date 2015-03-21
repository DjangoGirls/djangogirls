from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView


urlpatterns = patterns('',
    # Redirect old links:
    url(r'^pages/in-your-city/$', RedirectView.as_view(url='/organize/', permanent=True)),
    url(r'^admin$', RedirectView.as_view(url='/admin/', permanent=True)),

    # Regular links:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^community/', include('jobs.urls', namespace='jobs')),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'', include('core.urls', namespace='core')),
    url(r'', include('applications.urls', namespace='applications')),
    url(r'^ckeditor/', include('ckeditor.urls')),
)
