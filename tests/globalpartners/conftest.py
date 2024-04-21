from io import StringIO

import pytest

from globalpartners.models import GlobalPartner


@pytest.fixture
def out():
    out = StringIO()
    return out


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


@pytest.fixture
def partners():
    return GlobalPartner.objects.bulk_create(
        [
            GlobalPartner(
                company_name="Sherpany",
                contact_person="Jane Doe",
                contact_email="jane.doe@test.com",
                prospective_sponsor=True,
                contacted=False,
            ),
            GlobalPartner(
                company_name="DigitalOcean",
                contact_person="John Doe",
                contact_email="john@test.com",
                prospective_sponsor=True,
                contacted=True,
            ),
            GlobalPartner(
                company_name="PythonAnywhere",
                contact_person="Jane Doe",
                contact_email="jane@test.com",
                prospective_sponsor=False,
                patreon_sponsor=True,
                patreon_level_per_month=500,
                sponsor_level_annual=5000,
                contacted=False,
                promotional_materials_requested=False,
                is_active=True,
            ),
            GlobalPartner(
                company_name="3YourMind",
                contact_person="John Doe",
                contact_email="john@test.com",
                prospective_sponsor=False,
                patreon_sponsor=True,
                patreon_level_per_month=500,
                sponsor_level_annual=5000,
                contacted=True,
                promotional_materials_requested=True,
                is_active=True,
            ),
            GlobalPartner(
                company_name="Zapier",
                contact_person="John Doe",
                contact_email="john@test.com",
                prospective_sponsor=False,
                patreon_sponsor=True,
                patreon_level_per_month=500,
                sponsor_level_annual=5000,
                contacted=True,
                promotional_materials_requested=False,
                is_active=True,
            ),
            GlobalPartner(
                company_name="PostHog",
                contact_person="Jane Tes",
                contact_email="jane@test.com",
                prospective_sponsor=False,
                patreon_sponsor=False,
                sponsor_level_annual=1000,
                contacted=False,
                promotional_materials_requested=False,
                is_active=False,
                next_renewal_date="2024-02-15",
            ),
            GlobalPartner(
                company_name="Torchbox",
                contact_person="John Test",
                contact_email="test@test.com",
                prospective_sponsor=False,
                patreon_sponsor=False,
                sponsor_level_annual=500,
                contacted=True,
                promotional_materials_requested=False,
                is_active=True,
                next_renewal_date="2024-02-15",
            ),
            GlobalPartner(
                company_name="Mirumee",
                contact_person="Test Contact",
                contact_email="test@test.com",
                prospective_sponsor=False,
                sponsor_level_annual=2500,
                contacted=True,
                promotional_materials_requested=True,
                is_active=True,
                next_renewal_date="2024-02-15",
            ),
            GlobalPartner(
                company_name="Mirumee",
                contact_person="Test Contact",
                contact_email="test@test.com",
                prospective_sponsor=False,
                sponsor_level_annual=2500,
                contacted=True,
                promotional_materials_requested=False,
                is_active=False,
                next_renewal_date="2024-02-15",
            ),
        ]
    )
