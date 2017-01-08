from formtools.wizard.views import NamedUrlSessionWizardView
from django.shortcuts import redirect, render

from .forms import (
    PreviousEventForm, ApplicationForm, WorkshopForm, OrganizersForm)

# ORGANIZE FORM #

FORMS = (("previous_event", PreviousEventForm),
         ("application", ApplicationForm),
         ("organizers", OrganizersForm),
         ("workshop", WorkshopForm))

TEMPLATES = {"previous_event": "organize/form/step1_previous_event.html",
             "application": "organize/form/step2_application.html",
             "organizers": "organize/form/step3_organizers.html",
             "workshop": "organize/form/step4_workshop.html"}


class OrganizeFormWizard(NamedUrlSessionWizardView):

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        print("FINISHED")
        print(form_list)
        return redirect('organize:form_thank_you')


def skip_application_if_organizer(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('previous_event') or {}
    return cleaned_data.get('has_organized_before') != 'True'


organize_form_wizard = OrganizeFormWizard.as_view(
    FORMS,
    condition_dict={'application': skip_application_if_organizer},
    url_name='organize:form_step')

# ORGANIZE FORM #


def form_thank_you(request):
    return render(request, 'organize/form/thank_you.html', {})


def index(request):
    return render(request, 'organize/index.html', {})


def commitment(request):
    return render(request, 'organize/commitment.html', {})


def prerequisites(request):
    return render(request, 'organize/prerequisites.html', {})
