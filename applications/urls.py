from django.urls import path

from applications import views

app_name = "applications"
urlpatterns = [
    path("<slug:page_url>/apply/", views.apply, name="apply"),
    path("<slug:page_url>/applications/", views.application_list, name="applications"),
    path("<slug:page_url>/applications/<int:app_number>", views.application_detail, name="application_detail"),
    path("<slug:page_url>/applications/change_state/", views.change_state, name="change_state"),
    path("<slug:page_url>/applications/change_rsvp/", views.change_rsvp, name="change_rsvp"),
    path("<slug:page_url>/applications/download/", views.applications_csv, name="applications_csv"),
    path("<slug:page_url>/communication/", views.communication, name="communication"),
    path("<slug:page_url>/communication/compose/", views.compose_email, name="compose_email"),
    path("<slug:page_url>/communication/compose/<int:email_id>", views.compose_email, name="compose_email"),
    path("<slug:page_url>/rsvp/<slug:code>", views.rsvp, name="rsvp"),
]
