import pytest
import vcr
from django.conf import settings

from core import gmail_accounts
from core.models import Event


@pytest.fixture()
def veryrandom_event(future_event):
    return Event.objects.create(
        city=future_event.city, country=future_event.country, page_url="veryrandom", email="veryrandom@djangogirls.org"
    )


@pytest.fixture()
def second_veryrandom_event(future_event):
    future_event.email = "veryrandom@djangogirls.org"
    future_event.page_url = "veryrandom1"
    future_event.date = "2017-01-01"
    future_event.save()
    return future_event


def test_make_email():
    assert gmail_accounts.make_email("test") == "test@djangogirls.org"


@vcr.use_cassette("tests/core/vcr/gmail_accounts_create.yaml")
@pytest.mark.skipif(settings.GAPPS_PRIVATE_KEY == "", reason="No Gapps keys")
def test_create_gmail_account(second_veryrandom_event):
    email, password = gmail_accounts.create_gmail_account(second_veryrandom_event)
    assert email == second_veryrandom_event.email
    assert password is not None


@vcr.use_cassette("tests/core/vcr/gmail_accounts_get.yaml")
@pytest.mark.skipif(settings.GAPPS_PRIVATE_KEY == "", reason="No Gapps keys")
def test_get_gmail_account():
    response = gmail_accounts.get_gmail_account("veryrandom")
    assert response is None

    response = gmail_accounts.get_gmail_account("olasitarska")
    assert response is not None


@vcr.use_cassette("tests/core/vcr/gmail_accounts_migrate.yaml")
@pytest.mark.skipif(settings.GAPPS_PRIVATE_KEY == "", reason="No Gapps keys")
def test_migrate_gmail_account(second_veryrandom_event, veryrandom_event):
    old_email = second_veryrandom_event.email
    gmail_accounts.migrate_gmail_account(veryrandom_event, "veryrandom")

    second_veryrandom_event.refresh_from_db()
    veryrandom_event.refresh_from_db()

    assert old_email == veryrandom_event.email
    assert "veryrandom12017@djangogirls.org" == second_veryrandom_event.email
