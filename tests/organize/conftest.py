from datetime import date, timedelta

import pytest

from core.models import Event
from organize.constants import ON_HOLD
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
def past_event():
    return Event.objects.create(
        name="Django Girls Berlin",
        date="2014-06-21",
        city="Berlin",
        country="Germany",
        latlng='52.5170365, 13.3888599')


@pytest.fixture
def previous_organizer_remote(past_event):
    previous_event = {
        'previous_event-has_organized_before': True,
        'previous_event-previous_event': past_event.pk,
        'organize_form_wizard-current_step': 'previous_event'
    }
    organizers = {
        'organizers-TOTAL_FORMS': '2',
        'organizers-INITIAL_FORMS': '0',
        'organizers-MIN_NUM_FORMS': '1',
        'organizers-MAX_NUM_FORMS': '10',
        'organizers-0-email': 'test@test.com',
        'organizers-0-first_name': 'Anna',
        'organizers-0-last_name': 'Smith',
        'organizers-1-email': 'test1@test.com',
        'organizers-1-first_name': 'Jane',
        'organizers-1-last_name': 'Doe',
        'organize_form_wizard-current_step': 'organizers'
        }
    workshop_type = {
        'workshop_type-remote': True,
        'organize_form_wizard-current_step': 'workshop_type'
    }
    workshop_remote = {
        'workshop_remote-date': '2080-02-20',
        'workshop_remote-city': 'Luanda',
        'workshop_remote-country': 'AO',
        'workshop_remote-sponsorship': 'Yes, we hope to approach McKinsey and Accenture to sponsor our event.',
        'workshop_remote-coaches': 'I know a number of coaches from our local meet-up.',
        'workshop_remote-tools': 'We will use Zoom for video conferencing, share Google folder and GitHub to share links to resources.',
        'workshop_remote-diversity': 'Promote on social media and use videos',
        'workshop_remote-additional': 'None',
        'organize_form_wizard-current_step': 'workshop_remote'
    }

    data = (
        ('previous_event', previous_event),
        ('organizers', organizers),
        ('workshop_type', workshop_type),
        ('workshop_remote', workshop_remote)
    )

    return data


@pytest.fixture
def new_organizer_remote():
    previous_event = {
        'previous_event-has_organized_before': False,
        'organize_form_wizard-current_step': 'previous_event'
    }
    application = {
        'application-about_you': 'I am a volunteer for my local meet-up.',
        'application-why': 'I want to introduce more women to coding.',
        'application-involvement': 'coach, organizer',
        'application-experience': 'I organize our local meet-ups.',
        'organize_form_wizard-current_step': 'application'
    }
    organizers = {
        'organizers-TOTAL_FORMS': '2',
        'organizers-INITIAL_FORMS': '0',
        'organizers-MIN_NUM_FORMS': '1',
        'organizers-MAX_NUM_FORMS': '10',
        'organizers-0-email': 'test1@test.com',
        'organizers-0-first_name': 'Jane',
        'organizers-0-last_name': 'Doe',
        'organizers-1-email': 'test2@test.com',
        'organizers-1-first_name': 'John',
        'organizers-1-last_name': 'Doe',
        'organize_form_wizard-current_step': 'organizers'
    }
    workshop_type = {
        'workshop_type-remote': True,
        'organize_form_wizard-current_step': 'workshop_type'
    }
    workshop_remote = {
        'workshop_remote-date': '2080-05-28',
        'workshop_remote-city': 'Lilongwe',
        'workshop_remote-country': 'MW',
        'workshop_remote-sponsorship': 'Yes we have a few organizations we plan to approach.',
        'workshop_remote-coaches': 'Yes we have an active Python community already.',
        'workshop_remote-tools': 'We will use Zoom and GitHub.',
        'workshop_remote-diversity': 'Promote on social media and use videos',
        'workshop_remote-additional': 'No',
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
def previous_organizer_in_person(past_event):
    previous_event = {
        'previous_event-has_organized_before': True,
        'previous_event-previous_event': past_event.pk,
        'organize_form_wizard-current_step': 'previous_event'
    }
    organizers = {
        'organizers-TOTAL_FORMS': '2',
        'organizers-INITIAL_FORMS': '0',
        'organizers-MIN_NUM_FORMS': '1',
        'organizers-MAX_NUM_FORMS': '10',
        'organizers-0-email': 'jose@test.com',
        'organizers-0-first_name': 'Jose',
        'organizers-0-last_name': 'Jonas',
        'organizers-1-email': 'jonas@test.com',
        'organizers-1-first_name': 'Jonas',
        'organizers-1-last_name': 'Jose Jnr',
        'organize_form_wizard-current_step': 'organizers'
    }
    workshop_type = {
        'workshop_type-remote': False,
        'organize_form_wizard-current_step': 'workshop_type'
    }
    workshop = {
        'workshop-date': '2060-01-31',
        'workshop-city': 'Beira',
        'workshop-country': 'MZ',
        'workshop-venue': 'Beira Hall',
        'workshop-sponsorship': 'My employer will sponsor the event.',
        'workshop-coaches': 'My colleagues will coach at the event.',
        'workshop-safety': 'Social distancing',
        'workshop-diversity': 'Promote on social media and use videos',
        'workshop-additional': 'None',
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
        'previous_event-has_organized_before': False,
        'organize_form_wizard-current_step': 'previous_event'
    }
    application = {
        'application-about_you': 'I am a volunteer in my local meet-up.',
        'application-why': 'There are a few women who know how to code in our meet-up.',
        'application-involvement': 'coach',
        'application-experience': 'I have volunteered at my local meet-up.',
        'organize_form_wizard-current_step': 'application'
    }
    organizers = {
        'organizers-TOTAL_FORMS': '2',
        'organizers-INITIAL_FORMS': '0',
        'organizers-MIN_NUM_FORMS': '1',
        'organizers-MAX_NUM_FORMS': '10',
        'organizers-0-email': 'ana@test.com',
        'organizers-0-first_name': 'Ana',
        'organizers-0-last_name': 'Dona',
        'organizers-1-email': 'dona@test.com',
        'organizers-1-first_name': 'Dona',
        'organizers-1-last_name': 'Ana',
        'organize_form_wizard-current_step': 'organizers'
    }
    workshop_type = {
        'workshop_type-remote': False,
        'organize_form_wizard-current_step': 'workshop_type'
    }
    workshop = {
        'workshop-date': '2080-01-01',
        'workshop-city': 'Maputo',
        'workshop-country': 'MZ',
        'workshop-venue': 'Baixa Mall',
        'workshop-sponsorship': 'We have a few local companies we can approach.',
        'workshop-coaches': 'We have many Python developers here.',
        'workshop-safety': 'We will practise social distancing, wear masks and sanitize hands,',
        'workshop-diversity': 'Promote on social media and use videos',
        'workshop-additional': 'None',
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
        'diversity': 'Promote on social media and use videos',
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
        'diversity': 'Promote on social media and use videos',
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
        'diversity': 'Promote on social media and use videos',
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
        'diversity': 'Promote on social media and use videos',
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
        'diversity': 'Promote on social media and use videos',
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
        'diversity': 'Promote on social media and use videos',
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
        'diversity': 'Promote on social media and use videos',
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
        'diversity': 'Promote on social media and use videos',
        'additional': 'None',
    }
    return data


@pytest.fixture
def previous_application():
    return None


@pytest.fixture
def previous_event():
    return None


@pytest.fixture
def previous_application_more_than_6_months():
    return EventApplication.objects.create(
        city='Addis Ababa',
        country='Ethiopia',
        date='',
        created_at='',
        main_organizer_email='test@test.com',
        status='new'
    )


@pytest.fixture
def previous_application_less_than_6_months():
    return EventApplication.objects.create(
        city='Addis Ababa',
        country='Ethiopia',
        date='',
        created_at='',
        main_organizer_email='test@test.com',
        status='new'
    )


@pytest.fixture
def previous_event_in_6_months():
    return Event.objects.create(
        name="Django Girls Harare",
        date="2014-06-21",
        city="Harare",
        country="Zimbabwe",
        latlng='52.5170365, 13.3888599',
        main_organizer_email='test@test.com'
    )


@pytest.fixture
def previous_event_in_more_than_6_months():
    return Event.objects.create(
        name="Django Girls Harare",
        date="2016-04-16",
        city="Harare",
        country="Zimbabwe",
        latlng='52.5170365, 13.3888599',
        main_organizer_email='test@test.com'
    )


@pytest.fixture
def past_event():
    return None


@pytest.fixture
def past_application():
    return None

