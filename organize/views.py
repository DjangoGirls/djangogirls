from formtools.wizard.views import SessionWizardView
from django.shortcuts import redirect, render

from .forms import (
    PreviousEventForm, ApplicationForm, WorkshopForm, OrganizersForm)

FORMS = [("previous_event", PreviousEventForm),
         ("application", ApplicationForm),
         ("organizers", OrganizersForm)
         ("workshop", WorkshopForm)]

TEMPLATES = {"previous_event": "organize/form/step1_previous_event.html",
             "application": "organize/form/step2_application.html",
             "organizers": "organize/form/step4_organizers.html",
             "workshop": "organize/form/step3_workshop.html"}


class OrganizeFormWizard(SessionWizardView):
    form_list = FORMS

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        # do_something_with_the_form_data(form_list)
        return redirect('organize:form_thank_you')


def form_thank_you(request):
    return render(request, 'organize/form/thank_you.html', {})


def index(request):
    return render(request, 'organize/index.html', {})


def commitment(request):
    return render(request, 'organize/commitment.html', {})


def prerequisites(request):
    return render(request, 'organize/prerequisites.html', {})
