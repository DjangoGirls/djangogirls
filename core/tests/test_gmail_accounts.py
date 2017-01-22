import vcr
from django.test import TestCase

from core import gmail_accounts
from core.models import Event


class GmaillAccountsTestCase(TestCase):
    fixtures = ['core_views_testdata.json']

    def setUp(self):
        self.event = Event.objects.get(pk=1)
        self.event.email = "veryrandom@djangogirls.org"
        self.event.website_slug = "veryrandom"
        self.event.save()

    def test_make_email(self):
        assert gmail_accounts.make_email('test') == 'test@djangogirls.org'

    @vcr.use_cassette('core/tests/vcr/gmail_accounts_create.yaml')
    def test_create_gmail_account(self):
        email, password = gmail_accounts.create_gmail_account(self.event)
        assert email == self.event.email
        assert password is not None

    @vcr.use_cassette('core/tests/vcr/gmail_accounts_get.yaml', record_mode='new_episodes')
    def test_get_gmail_account(self):
        response = gmail_accounts.get_gmail_account('veryrandom')
        assert response is None

        response = gmail_accounts.get_gmail_account('olasitarska')
        assert response is not None

    @vcr.use_cassette('core/test/vcr/gmail_accounts_migrate.yaml')
    def test_migrate_gmail_account(self):
        old_email = self.event.email
        gmail_accounts.migrate_gmail_account('veryrandom')
        self.event.refresh_from_db()
        assert old_email is not self.event.email
