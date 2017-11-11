import pytest
import vcr
from django.conf import settings
from django.test import TestCase

from core import gmail_accounts
from core.models import Event


class GmaillAccountsTestCase(TestCase):
    fixtures = ['core_views_testdata.json']

    def setUp(self):
        self.event = Event.objects.get(pk=1)
        self.event.email = "veryrandom@djangogirls.org"
        self.event.page_url = "veryrandom1"
        self.event.date = "2017-01-01"
        self.event.save()

        self.new_event = Event.objects.create(
            city=self.event.city,
            country=self.event.country,
            page_url="veryrandom",
            email="veryrandom@djangogirls.org"
        )

    def test_make_email(self):
        assert gmail_accounts.make_email('test') == 'test@djangogirls.org'

    @vcr.use_cassette('tests/core/vcr/gmail_accounts_create.yaml')
    @pytest.mark.skipif(settings.GAPPS_PRIVATE_KEY == '', reason="No Gapps keys")
    def test_create_gmail_account(self):
        email, password = gmail_accounts.create_gmail_account(self.event)
        assert email == self.event.email
        assert password is not None

    @vcr.use_cassette('tests/core/vcr/gmail_accounts_get.yaml')
    @pytest.mark.skipif(settings.GAPPS_PRIVATE_KEY == '', reason="No Gapps keys")
    def test_get_gmail_account(self):
        response = gmail_accounts.get_gmail_account('veryrandom')
        assert response is None

        response = gmail_accounts.get_gmail_account('olasitarska')
        assert response is not None

    @vcr.use_cassette('tests/core/vcr/gmail_accounts_migrate.yaml')
    @pytest.mark.skipif(settings.GAPPS_PRIVATE_KEY == '', reason="No Gapps keys")
    def test_migrate_gmail_account(self):
        old_email = self.event.email
        gmail_accounts.migrate_gmail_account(self.new_event, 'veryrandom')

        self.event.refresh_from_db()
        self.new_event.refresh_from_db()

        assert old_email == self.new_event.email
        assert "veryrandom12017@djangogirls.org" == self.event.email
