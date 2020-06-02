from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('prerequisites/', views.prerequisites, name='prerequisites'),
    path('commitment/', views.commitment, name='commitment'),
    path('form/thank_you/', views.form_thank_you, name='form_thank_you'),
    path('form/<slug:step>/', views.organize_form_wizard, name='form_step'),
    path('suspend/', views.suspend, name='suspend')
]
