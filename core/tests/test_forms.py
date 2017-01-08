from core.forms import AddOrganizerForm
from core.models import Event
from django.test import TestCase


class AddOrganizerFormTestCase(TestCase):
    fixtures = ['core_views_testdata.json', 'groups_testdata.json']

    def test_name_splitting(self):
        event = Event.objects.first()
        form = AddOrganizerForm({
            'event': event.pk,
            'email': 'olaf@djangogirls.org',
            'name': 'Olaf Olaffson'
        })

        self.assertTrue(form.is_valid())
        organizer = form.save()
        self.assertEqual(organizer.first_name, 'Olaf')
        self.assertEqual(organizer.last_name, 'Olaffson')
