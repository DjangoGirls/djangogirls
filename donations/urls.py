from django.urls import path

from . import views

app_name = "donations"

urlpatterns = [
    path("", views.index, name="index"),
    path("charge/", views.charge, name="charge"),
    path("success/<str:currency>/<str:amount>/", views.success, name="success"),
    path("error/", views.error, name="error"),
    path("sponsors/", views.sponsors, name="sponsors"),
]
