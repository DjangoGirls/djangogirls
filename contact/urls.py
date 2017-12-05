from django.conf.urls import url

from contact.views import ContactView

app_name = "contact"
urlpatterns = [
    url(r'', ContactView.as_view(), name='contact'),
]
