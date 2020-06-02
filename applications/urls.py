from django.urls import path

from applications import views

app_name = 'applications'
urlpatterns = [
    path('<slug:city>/apply/', views.apply, name='apply'),
    path('<slug:city>/applications/',
         views.application_list, name='applications'),
    path('<slug:city>/applications/<int:app_number>',
         views.application_detail, name='application_detail'),
    path('<slug:city>/applications/change_state/',
         views.change_state, name='change_state'),
    path('<slug:city>/applications/change_rsvp/',
         views.change_rsvp, name='change_rsvp'),
    path('<slug:city>/applications/download/',
         views.applications_csv, name='applications_csv'),
    path('<slug:city>/communication/',
         views.communication, name='communication'),
    path('<slug:city>/communication/compose/',
         views.compose_email, name='compose_email'),
    path('<slug:city>/communication/compose/<int:email_id>',
         views.compose_email, name='compose_email'),
    path('<slug:city>/rsvp/<slug:code>', views.rsvp, name='rsvp'),
]
