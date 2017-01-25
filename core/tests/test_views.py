import os
from datetime import timedelta

from django.core import mail
from django.core.urlresolvers import reverse
from django.test import RequestFactory, TestCase
from django.test.client import Client
from django.utils import timezone
from django_date_extensions.fields import ApproximateDate
from contact.models import ContactEmail

from core.models import Event, User
from core.views import event as event_view


class BaseCoreTestCase(TestCase):
    fixtures = ['core_views_testdata.json', 'groups_testdata.json']

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        self.ola = User.objects.get(pk=1)
        self.peter = User.objects.get(pk=2)
        self.tinker = User.objects.get(pk=3)

        self.event_1 = Event.objects.get(pk=1)  # In the future
        self.event_2 = Event.objects.get(pk=2)  # In the past
        self.event_3 = Event.objects.get(pk=3)  # Hidden from homepage
        self.event_4 = Event.objects.get(pk=4)  # Not live, no date set
        self.events = [self.event_1, self.event_2, self.event_3, self.event_4]


class CoreViewsTestCase(BaseCoreTestCase):

    def test_index(self):
        # Access homepage
        resp = self.client.get(reverse('core:index'))
        self.assertEqual(resp.status_code, 200)

        # Check if it returns a list of past and future events
        self.assertTrue('past_events' and 'future_events' in resp.context)

        # Is future event on future list?
        self.assertEqual(
            [event.pk for event in resp.context['future_events']], [1])
        self.assertNotEqual(
            [event.pk for event in resp.context['future_events']], [2])

        # Is hidden event on the list?
        self.assertNotEqual(
            [event.pk for event in resp.context['future_events']], [3])

    def test_event_published(self):
        # Check if it's possible to access the page
        url1 = '/' + self.event_1.page_url + '/'
        resp_1 = self.client.get(url1)
        self.assertEqual(resp_1.status_code, 200)

        # Check if it's possible to access the page
        url2 = '/' + self.event_2.page_url + '/'
        resp_2 = self.client.get(url2)
        self.assertEqual(resp_2.status_code, 200)

        # Check if website is returning correct data
        self.assertTrue('page' and 'menu' and 'content' in resp_1.context)
        self.assertTrue('page' and 'menu' and 'content' in resp_2.context)

        # Check if not public content is not available in context:
        self.assertNotEqual(
            [content.pk for content in resp_1.context['content']], [1])

    def test_event_unpublished(self):
        # Check if accessing unpublished page renders the event_not_live page
        url = '/' + self.event_3.page_url + '/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        # Check if website is returning correct data
        self.assertTrue('city' and 'past' in resp.context)

    def test_event_unpublished_with_future_and_past_dates(self):
        future_date = timezone.now() + timedelta(days=1)
        past_date = timezone.now() - timedelta(days=1)

        # make the event date in the future
        self.event_4.date = ApproximateDate(
            year=future_date.year, month=future_date.month, day=future_date.day)
        self.event_4.save()

        # Check if accessing unpublished page renders the event_not_live page
        url = '/' + self.event_4.page_url + '/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        # Check if website is returning correct content
        self.assertIn('will be coming soon', str(
            resp.content), 'Incorrect content')

        # make the event date in the past
        self.event_4.date = ApproximateDate(
            year=past_date.year, month=past_date.month, day=past_date.day)
        self.event_4.save()

        # Check if accessing unpublished page renders the event_not_live page
        url = '/' + self.event_4.page_url + '/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        # Check if website is returning correct content
        self.assertIn('has already happened', str(
            resp.content), 'Incorrect content')

    def test_event_unpublished_with_authenticated_user(self):
        """ Test that an unpublished page can be accessed when the user is
        authenticated """

        url = '/' + self.event_3.page_url + '/'
        request = self.factory.get(url)

        # Set the user on the request to an authenticated user
        request.user = self.ola

        # Check if the unpublished page can be accessed
        resp = event_view(request, self.event_3.page_url)
        self.assertEqual(resp.status_code, 200)
        # Check if website is returning correct data
        self.assertIn(self.event_3.page_title, resp.content.decode('utf-8'))

    def test_coc(self):
        AVAILABLE_LANG = {
            'en': '<h1>Code of Conduct</h1>',
            'es': '<h1>Código de Conducta</h1>',
            'fr': '<h1>Code de Conduite</h1>',
            'ko': '<h1>준수 사항</h1>',
            'pt-br': '<h1>Código de Conduta</h1>'
        }
        for lang, title in AVAILABLE_LANG.items():
            resp = self.client.get('/coc/{}/'.format(lang))
            self.assertContains(resp, title, html=True)

    def test_coc_invalid_lang(self):
        resp = self.client.get('/coc/pl/')
        self.assertEqual(resp.status_code, 404)

    def test_coc_redirect(self):
        REDIRECTS = {
            'coc/': '/coc/',
            'coc-es-la/': '/coc/es/',
            'coc-fr/': '/coc/fr/',
            'coc-kr/': '/coc/ko/',
            'coc-pt-br/': '/coc/pt-br/',
            'coc/rec/': '/coc/pt-br/',
        }
        for old_url_name, new_url in REDIRECTS.items():
            old_url = reverse('django.contrib.flatpages.views.flatpage', args=[old_url_name])
            resp = self.client.get(old_url)
            self.assertRedirects(resp, new_url, status_code=301)


class ContactTestCase(TestCase):
    fixtures = ['core_views_testdata.json']

    def setUp(self):
        os.environ['RECAPTCHA_TESTING'] = 'True'

    def tearDown(self):
        del os.environ['RECAPTCHA_TESTING']

    def test_contact_page_loads(self):
        url = reverse('contact:contact')
        resp = self.client.get(url)
        self.assertEqual(200, resp.status_code)

    def test_form_sends_email_to_support(self):
        url = reverse('contact:contact')
        post_data = {
            'name': 'test name',
            'message': 'nice message',
            'email': 'lord@dracula.trans',
            'contact_type': ContactEmail.SUPPORT,
            'g-recaptcha-response': 'PASSED',
        }
        resp = self.client.post(url, data=post_data)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]

        self.assertEqual(email.to, ['hello@djangogirls.org'])
        self.assertEqual(email.reply_to, ['test name <lord@dracula.trans>'])
        self.assertEqual(email.body, 'nice message')

    def test_form_sends_email_to_chapter(self):
        event = Event.objects.get(pk=1)
        event.email = 'test@test.com'
        event.save()

        url = reverse('contact:contact')
        post_data = {
            'name': 'test name',
            'message': 'nice message',
            'email': 'lord@dracula.trans',
            'contact_type': ContactEmail.CHAPTER,
            'event': "1",
            'g-recaptcha-response': 'PASSED',
        }
        resp = self.client.post(url, data=post_data)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]

        self.assertEqual(email.to, ['test@test.com'])
        self.assertEqual(email.reply_to, ['test name <lord@dracula.trans>'])
        self.assertEqual(email.body, 'nice message')

    def test_chapter_contact_requires_event(self):
        url = reverse('contact:contact')
        post_data = {
            'name': 'test name',
            'message': 'nice message',
            'email': 'lord@dracula.trans',
            'contact_type': ContactEmail.CHAPTER,
            'event': "",
        }
        resp = self.client.post(url, data=post_data)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(len(mail.outbox), 0)
        self.assertIn('event', resp.context['form'].errors)
        self.assertFalse(ContactEmail.objects.all())

    def test_email_is_saved_into_database(self):
        event = Event.objects.get(pk=1)
        self.assertFalse(ContactEmail.objects.all())
        url = reverse('contact:contact')
        post_data = {
            'name': 'test name',
            'message': 'nice message',
            'email': 'lord@dracula.trans',
            'contact_type': ContactEmail.CHAPTER,
            'event': event.pk,
            'g-recaptcha-response': 'PASSED',
        }
        resp = self.client.post(url, data=post_data)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(1, ContactEmail.objects.all().count())

        contact_email = ContactEmail.objects.all()[0]
        self.assertTrue(contact_email.name, 'test name')
        self.assertTrue(contact_email.sent_to, 'hello@djangogirls.org')
        self.assertTrue(contact_email.message, 'nice message')
        self.assertTrue(contact_email.email, 'lord@dracula.trans')
        self.assertTrue(contact_email.event, event)
        self.assertTrue(contact_email.contact_type, ContactEmail.CHAPTER)
