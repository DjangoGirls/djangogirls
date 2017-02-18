from django.test import TestCase

from organize.models import EventApplication


EVENT_FIELDS = ['date', 'city', 'country', 'latlng']


class EventApplicationTest(TestCase):
    fixtures = ['event_application_testdata.json', 'pictures_testdata.json']

    def test_create_event(self):
        event_application = EventApplication.objects.get(pk=1)
        event = event_application.create_event()

        # we explicitly list the name of fields below, instead of using
        # getattr, to make the tests more beginners-friendly
        self.assertEquals(event.date, event_application.date)
        self.assertEquals(event.city, event_application.city)
        self.assertEquals(event.country, event_application.country)
        self.assertEquals(event.latlng, event_application.latlng)
        self.assertEquals(event.page_url, event_application.website_slug)

        name = "Django Girls {}".format(event.city)
        email = "{}@djangogirls.org".format(event.page_url)
        self.assertEquals(event.name, name)
        self.assertEquals(event.page_title, name)
        self.assertEquals(event.email, email)

        # check that we populate content from default event
        expected_content_sections = [
            'about', 'values', 'apply', 'faq', 'coach', 'partners', 'footer'
        ]
        self.assertEquals(
            set([e.name for e in event.content.all()]),
            set(expected_content_sections)
        )

        # check that we populate menu from default event
        self.assertTrue(event.menu.count() > 0)
        expected_menu_items = [
            'About', 'Apply for a pass!', 'FAQ', 'Become a coach', 'Partners'
        ]
        self.assertEquals(
            set([e.title for e in event.menu.all()]),
            set(expected_menu_items)
        )

        # check that we add a cover pictures
        self.assertTrue(event.photo)
        self.assertTrue(event.photo_credit)
        self.assertTrue(event.photo_link)
