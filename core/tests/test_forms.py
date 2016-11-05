from django.core import mail
from django.test import TestCase

from core.models import Event, User
from core.forms import AddOrganizerForm


class TestAddOrganizerForm(TestCase):

    def setUp(self):
        self.event = Event.objects.create(name='Test',
                                          city='Test',
                                          country='Test')
        # self.user = User.objects.create_user('test', password='SecretPassword')

    def test_notify_new_user(self):
        form = AddOrganizerForm(data={'event': self.event,
                                      'organizer': 'test',
                                      'email': 'test@test.com'})
        if(form.is_valid()):
            user = form.save()
            form.notify_new_user(user)
            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(mail.outbox[0].content_type, 'text/html')

    def test_notify_exisiting_user(self):
        form = AddOrganizerForm({'event': self.event,
                                 'organizer': 'Test',
                                 'email': 'test@test.com'})
        if(form.is_valid()):
            user = form.save()
            form.notify_existing_user(user)
            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(mail.outbox[0].content_type, 'text/html')
