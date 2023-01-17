from django.urls import path

from contact.views import ContactView

app_name = "contact"
urlpatterns = [
    path("", ContactView.as_view(), name="landing"),
]
