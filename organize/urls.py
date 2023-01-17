from django.urls import path

from . import views

app_name = "organize"
urlpatterns = [
    path("", views.index, name="index"),
    path("prerequisites/", views.prerequisites, name="prerequisites"),
    path("commitment/", views.commitment, name="commitment"),
    path("form/thank_you/", views.form_thank_you, name="form_thank_you"),
    path("form/<slug:step>/", views.organize_form_wizard, name="form_step"),
    # path('remote_or_in_person/', views.remote_or_in_person, name='remote_or_in_person'),
    path("suspend/", views.suspend, name="suspend"),
]
