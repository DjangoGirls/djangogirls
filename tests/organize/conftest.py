from datetime import date, timedelta

import pytest

from organize.constants import ON_HOLD
from organize.forms import (
    ApplicationForm, OrganizersFormSet, PreviousEventForm, RemoteWorkshopForm, WorkshopForm, WorkshopTypeForm)
from organize.models import EventApplication, Coorganizer


@pytest.fixture
def base_application():
    return EventApplication.objects.create(
        date="2080-10-10",
        city="London",
        country="Country",
        latlng='0.0,0.0',
        main_organizer_email="test@example.com",
        main_organizer_first_name="Anna",
        main_organizer_last_name="Smith")


@pytest.fixture
def application_with_coorganizer(base_application):
    Coorganizer.objects.create(
        event_application=base_application,
        email="anna@example.com",
        first_name="Anna",
        last_name="Smith")
    return base_application


@pytest.fixture
def application_on_hold(base_application):
    base_application.status = ON_HOLD
    base_application.save()

    return base_application


@pytest.fixture
def form_list_remote_previous_organizer():
    forms = (("previous_event", PreviousEventForm),
             ("organizers", OrganizersFormSet),
             ("workshop_type", WorkshopTypeForm),
             ("workshop_remote", RemoteWorkshopForm))
    return forms


@pytest.fixture
def form_list_remote_new_organizer():
    forms = (("previous_event", PreviousEventForm),
             ("application", ApplicationForm),
             ("organizers", OrganizersFormSet),
             ("workshop_type", WorkshopTypeForm),
             ("workshop_remote", RemoteWorkshopForm))
    return forms


@pytest.fixture
def form_list_previous_organizer():
    forms = (("previous_event", PreviousEventForm),
             ("organizers", OrganizersFormSet),
             ("workshop_type", WorkshopTypeForm),
             ("workshop", WorkshopForm))
    return forms


@pytest.fixture
def form_list_new_organizer():
    forms = (("previous_event", PreviousEventForm),
             ("application", ApplicationForm),
             ("organizers", OrganizersFormSet),
             ("workshop_type", WorkshopTypeForm),
             ("workshop", WorkshopForm))
    return forms


@pytest.fixture
def condition_dict_remote_previous_organizer():
    condition_dict = {
        'application': True,
        'workshop': True,
        'workshop_remote': False
    }
    return condition_dict


@pytest.fixture
def condition_dict_remote_new_organizer():
    condition_dict = {
        'application': False,
        'workshop': True,
        'workshop_remote': False
    }
    return condition_dict


@pytest.fixture
def condition_dict_previous_organizer():
    condition_dict = {
        'application': True,
        'workshop': False,
        'workshop_remote': True
    }
    return condition_dict


@pytest.fixture
def condition_dict_new_organizer():
    condition_dict = {
        'application': False,
        'workshop': False,
        'workshop_remote': True
    }
    return condition_dict


@pytest.fixture
def previous_organizer_remote():
    previous_event = {
        'previous_event': '<Event: Django Girls Berlin, 21st July 2014>',
        'organize_form_wizard-current_step': 'previous_event'
    }
    organizers = {
        'main_organizer_email': 'test@test.com',
        'main_organizer_first_name': 'Anna',
        'main_organizer_last_name': 'Smith',
        'coorganizers': [{'email': 'test1@test.com', 'first_name': 'Jane', 'last_name': 'Doe'}],
        'organize_form_wizard-current_step': 'organizers'
    }
    workshop_type = {
        'remote': True,
        'organize_form_wizard-current_step': 'workshop-type'
    }
    workshop_remote = {
        'date': '2080-02-20',
        'city': 'Luanda',
        'country': 'AO',
        'sponsorship': 'Yes, we hope to approach McKinsey and Accenture to sponsor our event.',
        'coaches': 'I know a number of coaches from our local meet-up.',
        'tools': 'We will use Zoom for video conferencing, share Google folder and GitHub to share links to resources.',
        'additional': 'None',
        'organize_form_wizard-current_step': 'workshop_remote'
    }

    application_data = (
        ('previous_event', previous_event),
        ('organizers', organizers),
        ('workshop_type', workshop_type),
        ('workshop_remote', workshop_remote)
    )

    return application_data


@pytest.fixture
def new_organizer_remote():
    previous_event = {
        'previous_event': None,
        'organize_form_wizard-current_step': 'previous_event'
    }
    application = {
        'about_you': 'I am a volunteer for my local meet-up.',
        'why': 'I want to introduce more women to coding.',
        'involvement': 'coach, organizer',
        'experience': 'I organize our local meet-ups.',
        'organize_form_wizard-current_step': 'application'
    }
    organizers = {
        'main_organizer_email': 'test1@test.com',
        'main_organizer_first_name': 'Jane',
        'main_organizer_last_name': 'Doe',
        'coorganizers': [{'email': 'test2@test.com', 'first_name': 'John', 'last_name': 'Doe'}],
        'organize_form_wizard-current_step': 'organizers'
    }
    workshop_type = {
        'remote': True,
        'organize_form_wizard-current_step': 'workshop_type'
    }
    workshop_remote = {
        'date': '2080-05-28',
        'city': 'Lilongwe',
        'country': 'MW',
        'sponsorship': 'Yes we have a few organizations we plan to approach.',
        'coaches': 'Yes we have an active Python community already.',
        'tools': 'We will use Zoom and GitHub.',
        'additional': 'No',
        'organize_form_wizard-current_step': 'workshop_remote'
    }

    application_data = (
        ('previous_event', previous_event),
        ('application', application),
        ('organizers', organizers),
        ('workshop_type', workshop_type),
        ('workshop_remote', workshop_remote)
    )
    return application_data


@pytest.fixture
def previous_organizer_in_person():
    previous_event = {
        'previous_event': '<Event: Django Girls Berlin, 21st July 2014>',
        'organize_form_wizard-current_step': 'previous_event'
    }
    organizers = {
        'main_organizer_email': 'jose@test.com',
        'main_organizer_first_name': 'Jose',
        'main_organizer_last_name': 'Jonas',
        'coorganizers': [{'email': 'jonas@test.com', 'first_name': 'Jonas', 'last_name': 'Jose Jnr'}],
        'organize_form_wizard-current_step': 'organizers'
    }
    workshop_type = {
        'remote': False,
        'organize_form_wizard-current_step': 'workshop_type'
    }
    workshop = {
        'date': '2060-01-31',
        'city': 'Beira',
        'country': 'MZ',
        'venue': 'Beira Hall',
        'sponsorship': 'My employer will sponsor the event.',
        'coaches': 'My colleagues will coach at the event.',
        'safety': 'Social distancing',
        'additional': 'None',
        'organize_form_wizard-current_step': 'workshop'
    }

    application_data = (
        ('previous_event', previous_event),
        ('organizers', organizers),
        ('workshop_type', workshop_type),
        ('workshop', workshop)
    )
    return application_data


@pytest.fixture
def new_organizer_in_person():
    previous_event = {
        'previous_event': None,
        'organize_form_wizard-current_step': 'previous_event'
    }
    application = {
        'about_you': 'I am a volunteer in my local meet-up.',
        'why': 'There are a few women who know how to code in our meet-up.',
        'involvement': 'coach',
        'experience': 'I have volunteered at my local meet-up.',
        'organize_form_wizard-current_step': 'application'
    }
    organizers = {
        'main_organizer_email': 'ana@test.com',
        'main_organizer_first_name': 'Ana',
        'main_organizer_last_name': 'Dona',
        'coorganizers': [{'email': 'dona@test.com', 'first_name': 'Dona', 'last_name': 'Ana'}],
        'organize_form_wizard-current_step': 'organizers'
    }
    workshop_type = {
        'remote': False,
        'organize_form_wizard-current_step': 'workshop_type'
    }
    workshop = {
        'date': '2080-01-01',
        'city': 'Maputo',
        'country': 'MZ',
        'venue': 'Baixa Mall',
        'sponsorship': 'We have a few local companies we can approach.',
        'coaches': 'We have many Python developers here.',
        'safety': 'We will practise social distancing, wear masks and sanitize hands,',
        'additional': 'None',
        'organize_form_wizard-current_step': 'workshop'
    }

    application_data = (
        ('previous_event', previous_event),
        ('application', application),
        ('organizers', organizers),
        ('workshop_type', workshop_type),
        ('workshop', workshop)
    )
    return application_data


@pytest.fixture
def past_date():
    previous_event = {
        'previous_event': None,
        'organize_form_wizard-current_step': 'previous_event'
    }
    application = {
        'about_you': 'I am a Python Software Engineer.',
        'why': 'I want to introduce more women to coding.',
        'involvement': 'attendee coach',
        'experience': 'Never organised or attended open source community events before.',
        'organize_form_wizard-current_step': 'application'
    }
    organizers = {
        'main_organizer_email': 'maria@test.com',
        'main_organizer_first_name': 'Maria',
        'main_organizer_last_name': 'Rosa',
        'coorganizers': [{'email': 'rosa@test.com', 'first_name': 'Rosa', 'last_name': 'Maria'}],
        'organize_form_wizard-current_step': 'organizers'
    }
    workshop_type = {
        'remote': True,
        'organize_form_wizard-current_step': 'workshop_type'
    }
    workshop_remote = {
        'date': '2020-07-01',
        'city': 'Gweru',
        'country': 'ZW',
        'sponsorship': 'We have Midlands State University as our main sponsor.',
        'coaches': 'We have MSU Computer Science students as coaches.',
        'tools': 'We will use Zoom and GitHub.',
        'additional': 'None',
        'organize_form_wizard-current_step': 'workshop_remote'
    }

    application_data = (
        ('previous_event', previous_event),
        ('application', application),
        ('organizers', organizers),
        ('workshop_type', workshop_type),
        ('workshop_remote', workshop_remote)
    )
    return application_data


@pytest.fixture
def date_less_than_three_months_away():
    event_date = date.today() + timedelta(days=30)
    previous_event = {
        'previous_event': None,
        'organize_form_wizard-current_step': 'previous_event'
    }
    application = {
        'about_you': 'I am Python Software Engineer.',
        'why': 'I want to get more women to love coding.',
        'involvement': 'attendee',
        'experience': 'New to open source events.',
        'organize_form_wizard-current_step': 'application'
    }
    organizers = {
        'main_organizer_email': 'carolina@test.com',
        'main_organizer_first_name': 'Carolina',
        'main_organizer_last_name': 'Awilo',
        'coorganizers': [{'email': 'maria@test.com', 'first_name': 'Maria', 'last_name': 'Rosa'}],
        'organize_form_wizard-current_step': 'organizers'
    }
    workshop_type = {
        'remote': True,
        'organize_form_wizard-current_step': 'workshop_type'
    }
    workshop_remote = {
        'date':  '{0}-{1}-{2}'.format(event_date.year, event_date.month, event_date.day),
        'city': 'Gaberone',
        'country': 'BW',
        'sponsorship': 'We have willing sponsors starting with my employer.',
        'coaches': 'We know many international speakers who can coach remotely.',
        'tools': 'Will use Zoom and GitHub',
        'additional': 'None',
        'organize_form_wizard-current_step': 'workshop_remote'
    }

    application_data = (
        ('previous_event', previous_event),
        ('application', application),
        ('organizers', organizers),
        ('workshop_type', workshop_type),
        ('workshop_remote', workshop_remote)
    )
    return application_data


@pytest.fixture
def workshop_form_valid_date():
    event_date = date.today() + timedelta(days=100)
    data = {
        'date':  '{0}-{1}-{2}'.format(event_date.year, event_date.month, event_date.day),
        'city': 'Gaberone',
        'country': 'BW',
        'venue': 'Baixa Mall',
        'sponsorship': 'We have a few local companies we can approach.',
        'coaches': 'We have many Python developers here.',
        'safety': 'We will practise social distancing, wear masks and sanitize hands,',
        'additional': 'None'
    }
    return data


@pytest.fixture
def workshop_form_too_close():
    event_date = date.today() + timedelta(days=30)
    data = {
        'date':  '{0}-{1}-{2}'.format(event_date.year, event_date.month, event_date.day),
        'city': 'Gaberone',
        'country': 'BW',
        'venue': 'Baixa Mall',
        'sponsorship': 'We have a few local companies we can approach.',
        'coaches': 'We have many Python developers here.',
        'safety': 'We will practise social distancing, wear masks and sanitize hands,',
        'additional': 'None'
    }
    return data


@pytest.fixture
def workshop_form_past_date():
    data = {
        'date':  '2020-07-01',
        'city': 'Gaberone',
        'country': 'BW',
        'venue': 'Baixa Mall',
        'sponsorship': 'We have a few local companies we can approach.',
        'coaches': 'We have many Python developers here.',
        'safety': 'We will practise social distancing, wear masks and sanitize hands,',
        'additional': 'None'
    }
    return data


@pytest.fixture
def workshop_remote_form_valid_date():
    data = {
        'date':  '2070-01-30',
        'city': 'Gaberone',
        'country': 'BW',
        'sponsorship': 'We have willing sponsors starting with my employer.',
        'coaches': 'We know many international speakers who can coach remotely.',
        'tools': 'Will use Zoom and GitHub',
        'additional': 'None',
    }
    return data


@pytest.fixture
def workshop_remote_form_date_too_close():
    event_date = date.today() + timedelta(days=30)
    data = {
        'date':  '{0}-{1}-{2}'.format(event_date.year, event_date.month, event_date.day),
        'city': 'Gaberone',
        'country': 'BW',
        'sponsorship': 'We have willing sponsors starting with my employer.',
        'coaches': 'We know many international speakers who can coach remotely.',
        'tools': 'Will use Zoom and GitHub',
        'additional': 'None',
    }
    return data


@pytest.fixture
def workshop_remote_form_past_date():
    data = {
        'date':  '2020-07-01',
        'city': 'Gaberone',
        'country': 'BW',
        'sponsorship': 'We have willing sponsors starting with my employer.',
        'coaches': 'We know many international speakers who can coach remotely.',
        'tools': 'Will use Zoom and GitHub',
        'additional': 'None',
    }
    return data


@pytest.fixture
def workshop_form_date_year_only():
    data = {
        'date':  '2060',
        'city': 'Gaberone',
        'country': 'BW',
        'venue': 'Baixa Mall',
        'sponsorship': 'We have a few local companies we can approach.',
        'coaches': 'We have many Python developers here.',
        'safety': 'We will practise social distancing, wear masks and sanitize hands,',
        'additional': 'None'
    }
    return data


@pytest.fixture
def workshop_remote_form_date_year_only():
    data = {
        'date':  '2050',
        'city': 'Gaberone',
        'country': 'BW',
        'sponsorship': 'We have willing sponsors starting with my employer.',
        'coaches': 'We know many international speakers who can coach remotely.',
        'tools': 'Will use Zoom and GitHub',
        'additional': 'None',
    }
    return data


@pytest.fixture
def no_previous_application():
    previous_application = None
    return previous_application


@pytest.fixture
def previous_application_more_than_6_months():
    previous_application = {
        'city': 'Addis Ababa',
        'country': 'ET',
        'date': '',
        'main_organizer_email': 'test@test.com',
        'status': 'new'
    }
    return previous_application


@pytest.fixture
def previous_application_less_than_6_months():
    previous_application = {
        'city': 'Addis Ababa',
        'country': 'ET',
        'date': '',
        'main_organizer_email': 'test@test.com',
        'status': 'new'
    }
    return previous_application


@pytest.fixture
def no_previous_event():
    previous_event = None
    return previous_event


@pytest.fixture
def previous_event_in_6_months():
    previous_event = {
        'city': 'Harare',
        'country': 'ZW',
        'date': '',
        'main_organizer': 'test@test.com',
        'status': 'deployed'
    }
    return previous_event


@pytest.fixture
def previous_event_in_more_than_6_months():
    previous_event = {
        'city': 'Harare',
        'country': 'ZW',
        'date': '2016-04-16',
        'main_organizer_email': 'test@test.com',
        'status': 'deployed'
    }
    return previous_event
