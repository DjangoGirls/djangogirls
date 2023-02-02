import pytest


@pytest.fixture
def global_partner_data():
    data = {
        "company_name": "Django Software Foundation",
        "contact_person": "John Doe",
        "contact_email": "john@djangoproject.com",
        "prospective_sponsor": False,
        "patreon_sponsor": True,
        "patreon_level_per_month": 500,
        "sponsor_level_annual": 5000,
        "date_joined": "2015-10-12",
        "logo": "django.png",
        "is_displayed": True,
        "website_url": "https://www.djangoproject.com",
    }
    return data
