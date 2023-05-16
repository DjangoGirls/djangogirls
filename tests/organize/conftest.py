from datetime import date, datetime, timedelta

import pytest
from django_date_extensions.fields import ApproximateDate

from core.models import Event
from organize.constants import ON_HOLD
from organize.models import Coorganizer, EventApplication


@pytest.fixture()
def base_application():
    return EventApplication.objects.create(
        date="2080-10-10",
        city="London",
        country="Country",
        latlng="0.0,0.0",
        main_organizer_email="test@example.com",
        main_organizer_first_name="Anna",
        main_organizer_last_name="Smith",
    )


@pytest.fixture
def application_with_coorganizer(base_application):
    Coorganizer.objects.create(
        event_application=base_application, email="anna@example.com", first_name="Anna", last_name="Smith"
    )
    return base_application


@pytest.fixture
def application_on_hold(base_application):
    base_application.status = ON_HOLD
    base_application.save()

    return base_application


@pytest.fixture
def previous_organizer_remote(past_event):
    previous_event = {
        "previous_event-has_organized_before": True,
        "previous_event-previous_event": past_event.pk,
        "organize_form_wizard-current_step": "previous_event",
    }
    organizers = {
        "organizers-TOTAL_FORMS": "2",
        "organizers-INITIAL_FORMS": "0",
        "organizers-MIN_NUM_FORMS": "1",
        "organizers-MAX_NUM_FORMS": "10",
        "organizers-0-email": "peter-pan@example.com",
        "organizers-0-first_name": "Peter",
        "organizers-0-last_name": "Pan",
        "organizers-1-email": "test1@test.com",
        "organizers-1-first_name": "Jane",
        "organizers-1-last_name": "Doe",
        "organize_form_wizard-current_step": "organizers",
    }
    workshop_type = {"workshop_type-remote": True, "organize_form_wizard-current_step": "workshop_type"}
    workshop_remote = {
        "workshop_remote-date": "2080-02-20",
        "workshop_remote-city": "Luanda",
        "workshop_remote-country": "AO",
        "workshop_remote-sponsorship": "Yes, we hope to approach McKinsey and Accenture to sponsor our event.",
        "workshop_remote-coaches": "I know a number of coaches from our local meet-up.",
        "workshop_remote-tools": "We will use Zoom for video conferencing, share Google folder and GitHub to "
        "share links to resources.",
        "workshop_remote-diversity": "Promote on social media and use videos",
        "workshop_remote-additional": "None",
        "organize_form_wizard-current_step": "workshop_remote",
    }

    data = (
        ("previous_event", previous_event),
        ("organizers", organizers),
        ("workshop_type", workshop_type),
        ("workshop_remote", workshop_remote),
    )

    return data


@pytest.fixture
def new_organizer_remote():
    previous_event = {
        "previous_event-has_organized_before": False,
        "organize_form_wizard-current_step": "previous_event",
    }
    application = {
        "application-about_you": "I am a volunteer for my local meet-up.",
        "application-why": "I want to introduce more women to coding.",
        "application-involvement": "coach, organizer",
        "application-experience": "I organize our local meet-ups.",
        "organize_form_wizard-current_step": "application",
    }
    organizers = {
        "organizers-TOTAL_FORMS": "2",
        "organizers-INITIAL_FORMS": "0",
        "organizers-MIN_NUM_FORMS": "1",
        "organizers-MAX_NUM_FORMS": "10",
        "organizers-0-email": "test1@test.com",
        "organizers-0-first_name": "Jane",
        "organizers-0-last_name": "Doe",
        "organizers-1-email": "test2@test.com",
        "organizers-1-first_name": "John",
        "organizers-1-last_name": "Doe",
        "organize_form_wizard-current_step": "organizers",
    }
    workshop_type = {"workshop_type-remote": True, "organize_form_wizard-current_step": "workshop_type"}
    workshop_remote = {
        "workshop_remote-date": "2080-05-28",
        "workshop_remote-city": "Lilongwe",
        "workshop_remote-country": "MW",
        "workshop_remote-sponsorship": "Yes we have a few organizations we plan to approach.",
        "workshop_remote-coaches": "Yes we have an active Python community already.",
        "workshop_remote-tools": "We will use Zoom and GitHub.",
        "workshop_remote-diversity": "Promote on social media and use videos",
        "workshop_remote-additional": "No",
        "organize_form_wizard-current_step": "workshop_remote",
    }

    application_data = (
        ("previous_event", previous_event),
        ("application", application),
        ("organizers", organizers),
        ("workshop_type", workshop_type),
        ("workshop_remote", workshop_remote),
    )
    return application_data


@pytest.fixture
def previous_organizer_in_person(past_event):
    previous_event = {
        "previous_event-has_organized_before": True,
        "previous_event-previous_event": past_event.pk,
        "organize_form_wizard-current_step": "previous_event",
    }
    organizers = {
        "organizers-TOTAL_FORMS": "2",
        "organizers-INITIAL_FORMS": "0",
        "organizers-MIN_NUM_FORMS": "1",
        "organizers-MAX_NUM_FORMS": "10",
        "organizers-0-email": "peter-pan@example.com",
        "organizers-0-first_name": "Peter",
        "organizers-0-last_name": "Pan",
        "organizers-1-email": "jonas@test.com",
        "organizers-1-first_name": "Jonas",
        "organizers-1-last_name": "Jose Jnr",
        "organize_form_wizard-current_step": "organizers",
    }
    workshop_type = {"workshop_type-remote": False, "organize_form_wizard-current_step": "workshop_type"}
    workshop = {
        "workshop-date": "2080-02-20",
        "workshop-city": "Beira",
        "workshop-country": "MZ",
        "workshop-venue": "Beira Hall",
        "workshop-sponsorship": "My employer will sponsor the event.",
        "workshop-coaches": "My colleagues will coach at the event.",
        "workshop-local_restrictions": "All restrictions relaxed. https://somegov.gov",
        "workshop-safety": "Social distancing",
        "workshop-diversity": "Promote on social media and use videos",
        "workshop-additional": "None",
        "workshop-confirm_covid_19_protocols": True,
        "organize_form_wizard-current_step": "workshop",
    }

    application_data = (
        ("previous_event", previous_event),
        ("organizers", organizers),
        ("workshop_type", workshop_type),
        ("workshop", workshop),
    )
    return application_data


@pytest.fixture
def new_organizer_in_person():
    previous_event = {
        "previous_event-has_organized_before": False,
        "organize_form_wizard-current_step": "previous_event",
    }
    application = {
        "application-about_you": "I am a volunteer in my local meet-up.",
        "application-why": "There are a few women who know how to code in our meet-up.",
        "application-involvement": "coach",
        "application-experience": "I have volunteered at my local meet-up.",
        "organize_form_wizard-current_step": "application",
    }
    organizers = {
        "organizers-TOTAL_FORMS": "2",
        "organizers-INITIAL_FORMS": "0",
        "organizers-MIN_NUM_FORMS": "1",
        "organizers-MAX_NUM_FORMS": "10",
        "organizers-0-email": "ana@test.com",
        "organizers-0-first_name": "Ana",
        "organizers-0-last_name": "Dona",
        "organizers-1-email": "dona@test.com",
        "organizers-1-first_name": "Dona",
        "organizers-1-last_name": "Ana",
        "organize_form_wizard-current_step": "organizers",
    }
    workshop_type = {"workshop_type-remote": False, "organize_form_wizard-current_step": "workshop_type"}
    workshop = {
        "workshop-date": "2080-01-01",
        "workshop-city": "Maputo",
        "workshop-country": "MZ",
        "workshop-venue": "Baixa Mall",
        "workshop-sponsorship": "We have a few local companies we can approach.",
        "workshop-coaches": "We have many Python developers here.",
        "workshop-local_restrictions": "All restrictions relaxed. https://somegov.gov",
        "workshop-safety": "We will practise social distancing, wear masks and sanitize hands,",
        "workshop-diversity": "Promote on social media and use videos",
        "workshop-additional": "None",
        "workshop-confirm_covid_19_protocols": True,
        "organize_form_wizard-current_step": "workshop",
    }

    application_data = (
        ("previous_event", previous_event),
        ("application", application),
        ("organizers", organizers),
        ("workshop_type", workshop_type),
        ("workshop", workshop),
    )
    return application_data


@pytest.fixture
def workshop_form_valid_date():
    event_date = date.today() + timedelta(days=100)
    data = {
        "date": f"{event_date.year}-{event_date.month}-{event_date.day}",
        "city": "Gaberone",
        "country": "BW",
        "venue": "Baixa Mall",
        "sponsorship": "We have a few local companies we can approach.",
        "coaches": "We have many Python developers here.",
        "local_restrictions": "Maximum number of attendees is 50. https://somegovt.com/",
        "safety": "We will practise social distancing, wear masks and sanitize hands,",
        "diversity": "Promote on social media and use videos",
        "additional": "None",
        "confirm_covid_19_protocols": True,
    }
    return data


@pytest.fixture
def workshop_form_too_close():
    event_date = date.today() + timedelta(days=30)
    data = {
        "date": f"{event_date.year}-{event_date.month}-{event_date.day}",
        "city": "Gaberone",
        "country": "BW",
        "venue": "Baixa Mall",
        "sponsorship": "We have a few local companies we can approach.",
        "coaches": "We have many Python developers here.",
        "safety": "We will practise social distancing, wear masks and sanitize hands,",
        "diversity": "Promote on social media and use videos",
        "additional": "None",
    }
    return data


@pytest.fixture
def workshop_form_past_date():
    data = {
        "date": "2020-07-01",
        "city": "Gaberone",
        "country": "BW",
        "venue": "Baixa Mall",
        "sponsorship": "We have a few local companies we can approach.",
        "coaches": "We have many Python developers here.",
        "safety": "We will practise social distancing, wear masks and sanitize hands,",
        "diversity": "Promote on social media and use videos",
        "additional": "None",
    }
    return data


@pytest.fixture
def workshop_remote_form_valid_date():
    data = {
        "date": "2070-01-30",
        "city": "Gaberone",
        "country": "BW",
        "sponsorship": "We have willing sponsors starting with my employer.",
        "coaches": "We know many international speakers who can coach remotely.",
        "tools": "Will use Zoom and GitHub",
        "diversity": "Promote on social media and use videos",
        "additional": "None",
    }
    return data


@pytest.fixture
def workshop_remote_form_date_too_close():
    event_date = date.today() + timedelta(days=30)
    data = {
        "date": f"{event_date.year}-{event_date.month}-{event_date.day}",
        "city": "Gaberone",
        "country": "BW",
        "sponsorship": "We have willing sponsors starting with my employer.",
        "coaches": "We know many international speakers who can coach remotely.",
        "tools": "Will use Zoom and GitHub",
        "diversity": "Promote on social media and use videos",
        "additional": "None",
    }
    return data


@pytest.fixture
def workshop_remote_form_past_date():
    data = {
        "date": "2020-07-01",
        "city": "Gaberone",
        "country": "BW",
        "sponsorship": "We have willing sponsors starting with my employer.",
        "coaches": "We know many international speakers who can coach remotely.",
        "tools": "Will use Zoom and GitHub",
        "diversity": "Promote on social media and use videos",
        "additional": "None",
    }
    return data


@pytest.fixture
def workshop_form_date_year_only():
    data = {
        "date": "2060",
        "city": "Gaberone",
        "country": "BW",
        "venue": "Baixa Mall",
        "sponsorship": "We have a few local companies we can approach.",
        "coaches": "We have many Python developers here.",
        "safety": "We will practise social distancing, wear masks and sanitize hands,",
        "diversity": "Promote on social media and use videos",
        "additional": "None",
    }
    return data


@pytest.fixture
def workshop_remote_form_date_year_only():
    data = {
        "date": "2050",
        "city": "Gaberone",
        "country": "BW",
        "sponsorship": "We have willing sponsors starting with my employer.",
        "coaches": "We know many international speakers who can coach remotely.",
        "tools": "Will use Zoom and GitHub",
        "diversity": "Promote on social media and use videos",
        "additional": "None",
    }
    return data


@pytest.fixture
def previous_application_more_than_6_months():
    previous_application = EventApplication.objects.create(
        city="Addis Ababa",
        country="Ethiopia",
        date="2070-01-30",
        created_at=timedelta(days=-180),
        main_organizer_email="test@test.com",
        main_organizer_first_name="Anna",
        main_organizer_last_name="Smith",
        status="new",
    )
    return previous_application


@pytest.fixture
def previous_application_less_than_6_months():
    previous_application = EventApplication.objects.create(
        city="Addis Ababa",
        country="Ethiopia",
        date="2070-01-30",
        created_at=datetime.now(),
        main_organizer_email="test@test.com",
        main_organizer_first_name="Anna",
        main_organizer_last_name="Smith",
        status="new",
    )
    return previous_application


@pytest.fixture
def previous_event_more_than_6_months(organizer_peter):
    previous_event = Event.objects.create(
        email="harare@djangogirls.org",
        city="Harare",
        name="Django Girls Harare",
        country="Zimbabwe",
        latlng="-17.831773, 31.045686",
        is_on_homepage=True,
        main_organizer=organizer_peter,
        date="2016-04-16",
        page_url="harare",
        is_page_live=True,
    )
    previous_event.team.add(organizer_peter)
    return previous_event


@pytest.fixture
def data_dict(past_event):
    return {
        "previous_event": past_event,
        "main_organizer_email": "test@example.com",
        "main_organizer_first_name": "Anna",
        "main_organizer_last_name": "Smith",
        "remote": True,
        "date": ApproximateDate(2081, 3, 10),
        "city": "Harare",
        "country": "ZW",
        "sponsorship": "Yes",
        "coaches": "Yes",
        "tools": "Zoom",
        "diversity": "Reach out",
        "additional": "No",
    }


@pytest.fixture
def previous_deployed_application():
    return EventApplication.objects.create(
        city="Addis Ababa",
        country="Ethiopia",
        date="2080-10-10",
        created_at=datetime.now() - timedelta(days=181),
        main_organizer_email="test@example.com",
        main_organizer_first_name="Anna",
        main_organizer_last_name="Smith",
        status="deployed",
    )


@pytest.fixture
def workshop_form_invalid_no_link():
    event_date = date.today() + timedelta(days=100)
    data = {
        "date": f"{event_date.year}-{event_date.month}-{event_date.day}",
        "city": "Gaberone",
        "country": "BW",
        "venue": "Baixa Mall",
        "sponsorship": "We have a few local companies we can approach.",
        "coaches": "We have many Python developers here.",
        "local_restrictions": "Maximum number of attendees is 50 and social distancing of 1.5m apart.",
        "safety": "We will practise social distancing, wear masks and sanitize hands,",
        "diversity": "Promote on social media and use videos",
        "additional": "None",
        "confirm_covid_19_protocols": True,
    }
    return data


@pytest.fixture
def previous_deployed_event():
    return EventApplication.objects.create(
        city="Zanzibar",
        country="Tanzania",
        date="2070-10-10",
        created_at=datetime.now() - timedelta(days=181),
        main_organizer_email="test@example.com",
        main_organizer_first_name="Anna",
        main_organizer_last_name="Smith",
        status="deployed",
    )


@pytest.fixture
def previous_application_approximate_date():
    return EventApplication.objects.create(
        city="Zanzibar",
        country="Tanzania",
        date="2070-10-0",
        created_at=datetime.now() - timedelta(days=181),
        main_organizer_email="test@example.com",
        main_organizer_first_name="Anna",
        main_organizer_last_name="Smith",
        status="deployed",
    )
