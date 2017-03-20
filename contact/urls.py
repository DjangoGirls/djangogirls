from django.conf.urls import url

from contact.views import ContactView


urlpatterns = [
    url(r'^$', ContactView.as_view(), name='contact'),
]
