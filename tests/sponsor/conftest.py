import pytest

from sponsor.models import Donor, Sponsor


@pytest.fixture()
def donor():
    donor = Donor.objects.create(name="Ola", amount=50, visible=True)
    return donor


@pytest.fixture()
def sponsor():
    return Sponsor.objects.create(name="Company name")
