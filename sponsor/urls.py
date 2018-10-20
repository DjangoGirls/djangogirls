from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from sponsor.views import SponsorRequestView

app_name = "sponsor"
urlpatterns = [
    url(r'^sponsor-request/$', login_required(SponsorRequestView.as_view()),
        name='sponsor-request'),
]
