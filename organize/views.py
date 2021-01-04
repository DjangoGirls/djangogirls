from datetime import date, timedelta

from formtools.wizard.views import NamedUrlSessionWizardView
from django.shortcuts import redirect, render
from django.contrib import messages

from core.models import Event
from .emails import (
    send_application_confirmation, send_application_notification)
from .forms import (
    PreviousEventForm, ApplicationForm, WorkshopForm,  WorkshopTypeForm, RemoteWorkshopForm, OrganizersFormSet)
from .models import EventApplication
from.constants import NEW

# ORGANIZE FORM #

FORMS = (("previous_event", PreviousEventForm),
         ("application", ApplicationForm),
         ("organizers", OrganizersFormSet),
         ("workshop_type", WorkshopTypeForm),
         ("workshop", WorkshopForm),
         ("workshop_remote", RemoteWorkshopForm))

TEMPLATES = {"previous_event": "organize/form/step1_previous_event.html",
             "application": "organize/form/step2_application.html",
             "organizers": "organize/form/step3_organizers.html",
             "workshop_type": "organize/form/step4_workshop_type.html",
             "workshop": "organize/form/step5_workshop.html",
             "workshop_remote": "organize/form/step5_workshop_remote.html"}


class OrganizeFormWizard(NamedUrlSessionWizardView):

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        # Process the data from the forms
        data_dict = {}
        for form in form_list:
            data_dict.update(form.get_data_for_saving())
        organizers_data = data_dict.pop('coorganizers', [])

        # Check of main organizer has already applied to organise another event less than 6 months ago
        # or has hosted another workshop less than 6 month before
        # To solve problems of organizers submitting the form more than once.
        main_organizer_email = data_dict.get('main_organizer_email')
        today = date.today()
        event_date = data_dict.get('date')

        previous_application = EventApplication.objects.filter(main_organizer_email=main_organizer_email) \
            .filter(status=NEW).order_by('-created_at').first()

        previous_event = Event.objects.filter(main_organizer__email=main_organizer_email)\
            .order_by('-date').first()

        if previous_application:
            if today - date(previous_application.created_at.year,
                            previous_application.created_at.month,
                            previous_application.created_at.day) < timedelta(days=180):
                messages.error(self.request, 'You cannot apply to organize an event when you '
                                             'have another open application.')
                return redirect('organize:prerequisites')
        if previous_event:
            if date(event_date.year,
                    event_date.month,
                    event_date.day) - date(previous_event.date.year,
                                           previous_event.date.month,
                                           previous_event.date.day) < timedelta(days=180):
                messages.error(self.request, 'Your workshops should be 6 months apart. '
                                             'Please read our Organizer Manual')
                return redirect('organize:prerequisites')

        application = EventApplication.objects.create(**data_dict)
        for organizer in organizers_data:
            application.coorganizers.create(**organizer)
        send_application_confirmation(application)
        send_application_notification(application)
        return redirect('organize:form_thank_you')


def skip_application_if_organizer(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('previous_event') or {}
    return not cleaned_data.get('has_organized_before')


def skip_workshop_if_remote(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('workshop_type') or {}
    return not cleaned_data.get('remote')


def skip_workshop_remote_if_in_person(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('workshop_type') or {}
    return cleaned_data.get('remote', False)


organize_form_wizard = OrganizeFormWizard.as_view(
    FORMS,
    condition_dict={'application': skip_application_if_organizer,
                    'workshop': skip_workshop_if_remote,
                    'workshop_remote': skip_workshop_remote_if_in_person},
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


def suspend(request):
    return render(request, 'organize/suspend.html', {})
