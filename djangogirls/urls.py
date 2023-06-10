from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView
from django.views.i18n import JavaScriptCatalog

from core.views import coc_legacy

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    re_path(r"^coc/(?:(?P<lang>[a-z-]+)/)?$", coc_legacy, name="coc_legacy"),
    # Redirection for old CoC's flatpages:
    path("pages/coc/", RedirectView.as_view(url="/coc/", permanent=True)),
    path("pages/coc-es-la/", RedirectView.as_view(url="/coc/es/", permanent=True)),
    path("pages/coc-fr/", RedirectView.as_view(url="/coc/fr/", permanent=True)),
    path("pages/coc-kr/", RedirectView.as_view(url="/coc/ko/", permanent=True)),
    path("pages/coc-pt-br/", RedirectView.as_view(url="/coc/pt-br/", permanent=True)),
    path("pages/coc/rec/", RedirectView.as_view(url="/coc/pt-br/", permanent=True)),
]

urlpatterns += i18n_patterns(
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    # Redirect old links:
    path("pages/in-your-city/", RedirectView.as_view(url="/organize/", permanent=True)),
    path("admin", RedirectView.as_view(url="/admin/", permanent=True)),
    path("admin/core/eventpage/<int>/", RedirectView.as_view(pattern_name="admin:core_event_change")),
    # Admin link for password reset
    # See:
    # https://github.com/darklow/django-suit/blob/92a745d72935622220eca80edfce779419c30094/suit/templates/admin/
    # login.html#L61
    path(
        "admin/password_reset/",
        RedirectView.as_view(url="/account/password_reset", permanent=True),
        name="admin_password_reset",
    ),
    path("tinymce/", include("tinymce.urls")),
    # Regular links:
    path("admin/", admin.site.urls),
    path("pages/", include("django.contrib.flatpages.urls")),
    path("account/", include("django.contrib.auth.urls")),
    path("coach/", include("coach.urls")),
    path("contact/", include("contact.urls")),
    path("donate/", include("donations.urls")),
    path("organize/", include("organize.urls")),
    path("story/", include("story.urls")),
    path("jobs/", include("jobboard.urls")),
    # path('', include('sponsor.urls')),
    path("", include("applications.urls")),
    path("", include("core.urls")),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    try:
        import debug_toolbar

        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass
