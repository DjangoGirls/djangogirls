from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^prerequisites/$', views.prerequisites, name='prerequisites'),
    url(r'^commitment/$', views.commitment, name='commitment'),
    url(r'^form/$', views.OrganizeFormWizard.as_view(), name='form'),
    url(r'^form/thank_you/$', views.form_thank_you, name='form_thank_you'),
]
