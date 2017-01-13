from formtools.wizard.views import NamedUrlSessionWizardView
from django.shortcuts import redirect, render

from .forms import (
    PreviousEventForm, ApplicationForm, WorkshopForm, OrganizersFormSet)
from .models import Coorganizer, EventApplication

# ORGANIZE FORM #

FORMS = (("previous_event", PreviousEventForm),
         ("application", ApplicationForm),
         ("organizers", OrganizersFormSet),
         ("workshop", WorkshopForm))

TEMPLATES = {"previous_event": "organize/form/step1_previous_event.html",
             "application": "organize/form/step2_application.html",
             "organizers": "organize/form/step3_organizers.html",
             "workshop": "organize/form/step4_workshop.html"}


class OrganizeFormWizard(NamedUrlSessionWizardView):

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, form_dict, **kwargs):
        # Process the date from the forms
        data_dict = {}
        for key, form in form_dict.items():
            if key == "previous_event":
                del form.cleaned_data['has_organized_before']

            if key == "application":
                form.cleaned_data["involvement"] = (
                    ", ".form.cleaned_data.get('involvement'))

            if key == "organizers":
                organizers = [form.cleaned_data
                              for form in form.forms if form.has_changed()]
                main_organizer = organizers.pop(0)
                form.cleaned_data = {
                    'main_organizer_email': main_organizer['email'],
                    'main_organizer_first_name': main_organizer['first_name'],
                    'main_organizer_last_name': main_organizer['last_name']
                }

            data_dict.update(form.cleaned_data)

        application = EventApplication.objects.create(**data_dict)
        for organizer in organizers:
            application.coorganizers.create(**organizer)

        return redirect('organize:form_thank_you')


def skip_application_if_organizer(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('previous_event') or {}
    return not cleaned_data.get('has_organized_before')


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
