from datetime import timedelta

from django.test import TestCase, RequestFactory
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.utils import timezone
from django_date_extensions.fields import ApproximateDate

from core.models import Event, EventPage
from applications.models import Form
from applications.utils import DEFAULT_QUESTIONS

class ApplyView(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        self.event = Event.objects.create(name='Test', city='Test', country='Test')
        self.page = EventPage.objects.create(event=self.event, is_live=True, url='test')
        self.form = Form.objects.create(page=self.page)

    def test_access_apply_view(self):
        resp = self.client.get(reverse('applications:apply', args=['test']))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['form_obj'], self.form)
        self.assertEqual(len(resp.context['form'].fields), len(DEFAULT_QUESTIONS))

        # Redirect to event page because there is no form
        self.form.delete()
        resp = self.client.get(reverse('applications:apply', args=['test']))
        self.assertEqual(resp.status_code, 302)

        # Show 404 because there is no event page
        self.page.delete()
        resp = self.client.get(reverse('applications:apply', args=['test']))
        self.assertEqual(resp.status_code, 404)
