from django.conf.urls import url

from . import views

organize_form_wizard = views.OrganizeFormWizard.as_view(
    views.FORMS,
    url_name='organize:form_step')

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^prerequisites/$', views.prerequisites, name='prerequisites'),
    url(r'^commitment/$', views.commitment, name='commitment'),
    url(r'^form/thank_you/$', views.form_thank_you, name='form_thank_you'),
    url(r'^form/(?P<step>.+)/$', organize_form_wizard, name='form_step'),
    # url(r'^form/$', organize_form_wizard, name='form'),
]
