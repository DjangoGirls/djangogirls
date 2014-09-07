from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Redirect old links:
    url(r'^pages/in-your-city/$', RedirectView.as_view(url='/organize/', permanent=True)),
    url(r'^admin$', RedirectView.as_view(url='/admin/', permanent=True)),

    # Regular links:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'', include('core.urls', namespace='core')),
)
