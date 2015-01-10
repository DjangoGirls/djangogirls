from django.test import TestCase, RequestFactory
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.http import HttpRequest

from core.models import User, Event, EventPage, EventPageContent, EventPageMenu, Sponsor
from core.views import event

class CoreViewsTestCase(TestCase):

    fixtures = ['core_views_testdata.json']

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        self.ola = User.objects.get(pk=1)
        self.peter = User.objects.get(pk=2)
        self.tinker = User.objects.get(pk=3)

        self.event_1 = Event.objects.get(pk=1) # In the future
        self.event_2 = Event.objects.get(pk=2) # In the past
        self.event_3 = Event.objects.get(pk=3) # Hidden from homepage

    def test_index(self):
        # Access homepage
        resp = self.client.get(reverse('core:index'))
        self.assertEqual(resp.status_code, 200)

        # Check if it returns a list of past and future events
        self.assertTrue('past_events' and 'future_events' in resp.context)

        # Is future event on future list?
        self.assertEqual([event.pk for event in resp.context['future_events']], [1])
        self.assertNotEqual([event.pk for event in resp.context['future_events']], [2])

        # Is past event on past list?
        self.assertEqual([event.pk for event in resp.context['past_events']], [2])
        self.assertNotEqual([event.pk for event in resp.context['past_events']], [1])

        # Is hidden event on the list?
        self.assertNotEqual([event.pk for event in resp.context['past_events']], [3])
        self.assertNotEqual([event.pk for event in resp.context['future_events']], [3])

    def test_event_published(self):
        event_page_1 = EventPage.objects.get(event=self.event_1)
        event_page_2 = EventPage.objects.get(event=self.event_2)

        # Check if it's possible to access the page
        url1 = '/' + event_page_1.url + '/'
        resp_1 = self.client.get(url1)
        self.assertEqual(resp_1.status_code, 200)

        # Check if it's possible to access the page
        url2 = '/' + event_page_2.url + '/'
        resp_2 = self.client.get(url2)
        self.assertEqual(resp_2.status_code, 200)

        # Check if website is returing correct data
        self.assertTrue('page' and 'menu' and 'content' in resp_1.context)
        self.assertTrue('page' and 'menu' and 'content' in resp_2.context)

        # Check if not public content is not available in context:
        self.assertNotEqual([content.pk for content in resp_1.context['content']], [1])

    def test_event_unpublished(self):
        event_page_3 = EventPage.objects.get(event=self.event_3)
        # Check if accessing unpublished page raises 404
        url = '/' + event_page_3.url + '/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

        # Check 404 contains custom content
        self.assertIn("upcoming events", resp.content, "Content did not contain"
                                                       " custom 404 text")

    def test_event_unpublished_with_authenticated_user(self):
        """ Test that an unpublished page can be accessed when the user is
        authenticated """

        event_page_3 = EventPage.objects.get(event=self.event_3)
        url = '/' + event_page_3.url + '/'
        request = self.factory.get(url)

        # Set the user on the request to an authenticated user
        request.user = self.ola

        # Check if the unpublished page can be accessed
        resp = event(request, event_page_3.url)
        self.assertEqual(resp.status_code, 200)

