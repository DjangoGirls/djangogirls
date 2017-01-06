from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = [
    # Redirect old links:
    url(r'^pages/in-your-city/$', RedirectView.as_view(url='/organize/', permanent=True)),
    url(r'^admin$', RedirectView.as_view(url='/admin/', permanent=True)),
    url(r'^admin/core/eventpage/(\d+)/',
        RedirectView.as_view(pattern_name='admin:core_event_change')),

    # Admin link for password reset
    # See: https://github.com/darklow/django-suit/blob/92a745d72935622220eca80edfce779419c30094/suit/templates/admin/login.html#L61
    url(r'^admin/password_reset/$',
        RedirectView.as_view(url='/account/password_reset', permanent=True),
        name='admin_password_reset'),

    # Regular links:
    url(r'^community/', include('jobs.urls', namespace='jobs')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^account/', include('django.contrib.auth.urls')),
    url(r'', include('applications.urls', namespace='applications')),
    url(r'', include('core.urls', namespace='core')),
]
