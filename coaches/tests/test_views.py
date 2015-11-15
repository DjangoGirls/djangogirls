import json
from io import StringIO
import csv
from datetime import timedelta
from django.contrib.messages import get_messages
from django.test import TestCase, RequestFactory
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.utils import timezone
from core.models import Event, EventPage, User
from coaches.models import CoachForm, CoachApplication, Question, Answer
from coaches.utils import DEFAULT_QUESTIONS
from coaches.views import coach_applications, coach_application_detail
from django.http import HttpRequest


class RegisterAsCoachViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        self.event = Event.objects.create(name='Test', city='Test', country='Test')
        self.page = EventPage.objects.create(event=self.event, is_live=True, url='test')
        self.form = CoachForm.objects.create(page=self.page)

    def test_access_register_view(self):
        resp = self.client.get(reverse('coaches:register_as_coach', args=['test']))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['form_obj'], self.form)
        self.assertEqual(len(resp.context['form'].fields), len(DEFAULT_QUESTIONS))

        # Redirect to event page because there is no form
        self.form.delete()
        resp = self.client.get(reverse('coaches:register_as_coach', args=['test']))
        self.assertEqual(resp.status_code, 302)

        # Show 404 because there is no event page
        self.page.delete()
        resp = self.client.get(reverse('coaches:register_as_coach', args=['test']))
        self.assertEqual(resp.status_code, 404)

    def test_coach_application_not_open(self):
        now = timezone.now()
        self.form.open_from = now + timedelta(days=1)
        self.form.open_until = now + timedelta(days=2)
        self.form.save()

        resp = self.client.get(reverse('coaches:register_as_coach', args=['test']))
        self.assertEqual(resp.status_code, 302)

    def test_coach_application_open(self):
        now = timezone.now()
        self.form.open_from = now - timedelta(days=1)
        self.form.open_until = now + timedelta(days=1)
        self.form.save()

        resp = self.client.get(reverse('coaches:register_as_coach', args=['test']))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['form_obj'], self.form)

    def test_coach_application_not_open_organiser(self):
        now = timezone.now()
        self.form.open_from = now + timedelta(days=1)
        self.form.open_until = now + timedelta(days=2)
        self.form.save()

        user = User.objects.create(email='test@user.com', is_active=True)
        user.set_password('test')
        user.save()
        self.client.login(email='test@user.com', password='test')

        self.event.team.add(user)
        self.event.save()

        resp = self.client.get(reverse('coaches:register_as_coach', args=['test']))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['form_obj'], self.form)

    def test_coach_application_not_open_super_user(self):
        now = timezone.now()
        self.form.open_from = now + timedelta(days=1)
        self.form.open_until = now + timedelta(days=2)
        self.form.save()

        user = User.objects.create(email='test@user.com', is_active=True, is_staff=True, is_superuser=True)
        user.set_password('test')
        user.save()
        self.client.login(email='test@user.com', password='test')

        resp = self.client.get(reverse('coaches:register_as_coach', args=['test']))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['form_obj'], self.form)

    def test_registration_post(self):
        now = timezone.now()
        self.form.open_from = now - timedelta(days=1)
        self.form.open_until = now + timedelta(days=1)
        self.form.save()
        response = self.client.post('/test/register_as_coach/', {
            'question_1': 'Tom Ford',
            'question_2': 'tomford@tom.com',
            'question_3': '89089786786768',
            'question_4': 'Mac OS X',
            'question_4': 'Windows',
            'question_5': 'Yes',
            'question_6': 'With basic HTML/CSS knowledge',
            'question_6': "I'm flexible",
            'question_7': 'bla bla bla bla',
            'question_9': "I've read and understood the Django Girls Code of Conduct"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form_obj'], self.form)

        messages = get_messages(response)
        for message in messages:
            self.assertEqual(message.tags, "success")
            self.assertTrue("Yay! Your registration has been saved. You'll hear from us soon!" in message.message)


class CoachApplicationsView(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        self.event = Event.objects.create(name='Test', city='Test', country='Test')
        self.page = EventPage.objects.create(event=self.event, is_live=True, url='test')
        self.form = CoachForm.objects.create(page=self.page)
        self.form_2 = CoachForm.objects.create(page=self.page)
        self.user = User.objects.create(email='test@user.com', is_active=True, is_staff=True)
        self.user.set_password('test')
        self.user_2 = User.objects.create(email='test2@user.com')

        self.application_1 = CoachApplication.objects.create(form=self.form, state='submitted')
        self.application_2 = CoachApplication.objects.create(form=self.form, state='accepted')
        self.application_3 = CoachApplication.objects.create(form=self.form, state='rejected')

        self.url = reverse('coaches:coach_applications', args=['test'])

    def test_access_coach_applications_view(self):
        # as anonymous user
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

        # as logged in user, but not organiser of given event
        request = self.factory.get(self.url)
        request.user = self.user
        resp = coach_applications(request, city='test')
        self.assertEqual(resp.status_code, 404)

        # as superuser
        self.user.is_superuser = True
        self.user.save()
        request = self.factory.get(self.url)
        request.user = self.user
        resp = coach_applications(request, city='test')
        self.assertEqual(resp.status_code, 200)

        # as organiser of given event
        self.user.is_superuser = False
        self.user.save()
        self.event.team.add(self.user)
        self.event.save()
        request = self.factory.get(self.url)
        request.user = self.user
        resp = coach_applications(request, city='test')
        self.assertEqual(resp.status_code, 200)

    def test_organiser_only_decorator_without_city(self):
        request = self.factory.get('')
        request.user = self.user
        with self.assertRaises(ValueError):
            resp = coach_applications(request, city=None)

    def test_get_coach_applications_list(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.login(email='test@user.com', password='test')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['applications']), 3)

        # change one application's form
        self.application_1.form = self.form_2
        self.application_1.save()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['applications']), 2)

    def test_organiser_menu_in_coach_applications_list(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.login(email='test@user.com', password='test')
        resp = self.client.get(self.url)
        self.assertContains(
            resp,
            '<li><a href="/test/applications/">Attendee Applications</a></li>',
            html=True,
        )
        self.assertContains(
            resp,
            '<li><a href="/test/communication/">Applicant Messaging</a></li>',
            html=True,
        )
        self.assertContains(
            resp,
            '<li><a href="/test/coach_applications/">Coach Applications</a></li>',
            html=True,
        )
        self.assertContains(
            resp,
            '<li><a href="/test/coach_communication/">Coach Messaging</a></li>',
            html=True,
        )

    def get_filtered_coach_applications_list(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.login(email='test@user.com', password='test')

        # No filter
        resp = self.client.get(self.url)
        self.assertEqual(len(resp.context['applications']), 4)

        # Filter by submitted
        resp.self.client.get('{}?state=submitted'.format(self.url))
        self.assertEqual(len(resp.context['applications']), 1)
        self.assertEqual(resp.context['applications'], [self.application_1])

        # Filter by accepted
        resp.self.client.get('{}?state=accepted'.format(self.url))
        self.assertEqual(len(resp.context['applications']), 1)
        self.assertEqual(resp.context['applications'], [self.application_2])

        # Filter by rejected
        resp.self.client.get('{}?state=rejected'.format(self.url))
        self.assertEqual(len(resp.context['applications']), 1)
        self.assertEqual(resp.context['applications'], [self.application_3])

    def test_changing_coach_application_status(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.login(email='test@user.com', password='test')

        self.assertEqual(self.application_1.state, 'submitted')
        resp = self.client.post(
            reverse('coaches:change_coach_state', args=['test']),
            {'state': 'accepted', 'application': self.application_1.id}
        )
        self.assertEqual(resp.status_code, 200)
        self.application_1 = CoachApplication.objects.get(id=self.application_1.id)
        self.assertEqual(self.application_1.state, 'accepted')

    def test_changing_coach_application_status_errors(self):
        # user without permissions:
        resp = self.client.post(
            reverse('coaches:change_coach_state', args=['test']),
            {'state': 'accepted', 'application': self.application_1.id}
        )
        self.assertEqual(resp.status_code, 302)

        self.user.is_superuser = True
        self.user.save()
        self.client.login(email='test@user.com', password='test')

        # lack of state parameter
        resp = self.client.post(
            reverse('coaches:change_coach_state', args=['test']),
            {'application': self.application_1.id}
        )
        self.assertTrue('error' in json.loads(resp.content.decode('utf-8')))

        # lack of application parameter
        resp = self.client.post(
            reverse('coaches:change_coach_state', args=['test']),
            {'state': 'accepted'}
        )
        self.assertTrue('error' in json.loads(resp.content.decode('utf-8')))

    def changing_coach_application_status_in_bulk(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.login(email='test@user.com', password='test')

        self.assertEqual(self.application_1.state, 'submitted')
        self.assertEqual(self.application_3.state, 'rejected')
        resp = self.client.post(
            reverse('coaches:change_coach_state', args=['test']),
            {'state': 'accepted', 'application': [self.application_1.id, self.application_3.id]}
        )
        self.assertEqual(resp.status_code, 200)
        self.application_1 = CoachApplication.objects.get(id=self.application_1.id)
        self.application_3 = CoachApplication.objects.get(id=self.application_3.id)
        self.assertEqual(self.application_1.state, 'accepted')
        self.assertEqual(self.application_3.state, 'accepted')


class CoachApplicationsDownloadView(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        self.event = Event.objects.create(name='Test', city='Test', country='Test')
        self.page = EventPage.objects.create(event=self.event, is_live=True, url='test')
        self.form = CoachForm.objects.create(page=self.page)

        self.user = User.objects.create(email='test@user.com', is_active=True, is_staff=True)
        self.user.set_password('test')

        self.application_1 = CoachApplication.objects.create(form=self.form, state='submitted')
        self.application_2 = CoachApplication.objects.create(form=self.form, state='accepted')
        self.application_3 = CoachApplication.objects.create(form=self.form, state='rejected')

        self.last_question = self.form.question_set.last()
        self.application_1_last_answer = Answer.objects.create(
            application=self.application_1,
            question=self.last_question,
            answer='answer to last for app 1'
        )

        self.url = reverse('coaches:coach_applications_csv', args=['test'])

    def test_download_coach_applications_list(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.login(email='test@user.com', password='test')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEquals(
            resp.get('Content-Disposition'),
            'attachment; filename="test.csv"'
        )
        csv_file = StringIO(resp.content.decode('utf-8'))
        reader = csv.reader(csv_file)
        csv_list = list(reader)
        self.assertEquals(len(csv_list), 4)
        self.assertEquals(len(csv_list[0]), 11)
        self.assertEquals(csv_list[0][0], "Application Number")
        self.assertEquals(csv_list[1][1], "submitted")
        self.assertEquals(csv_list[2][1], "accepted")
        self.assertEquals(csv_list[3][1], "rejected")
        self.assertEquals(csv_list[1][10], "answer to last for app 1")

    def test_download_coach_applications_list_uses_query_parameters_to_filter_applications(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.login(email='test@user.com', password='test')
        resp = self.client.get(self.url + '?state=submitted&state=accepted')
        self.assertEqual(resp.status_code, 200)
        self.assertEquals(
            resp.get('Content-Disposition'),
            'attachment; filename="test.csv"'
        )
        csv_file = StringIO(resp.content.decode('utf-8'))
        reader = csv.reader(csv_file)
        csv_list = list(reader)
        self.assertEquals(len(csv_list), 3)

    def test_download_coach_applications_list_with_question_added(self):

        # add new question x as next to last question
        self.question_x = Question.objects.create(form=self.form,
                                                  question_type='text',
                                                  order=self.last_question.order,
                                                  title='questionx')
        self.last_question.order += 1
        self.last_question.save()

        # now create a new application with answer to the new question
        self.application_5 = CoachApplication.objects.create(form=self.form, state='submitted')
        self.application_5_x_answer = Answer.objects.create(application=self.application_5,
                                                            question=self.question_x,
                                                            answer='answer to questionx for app 5')
        self.application_5_last_answer = Answer.objects.create(application=self.application_5,
                                                               question=self.last_question,
                                                               answer='answer to last for app 5')
        self.user.is_superuser = True
        self.user.save()
        self.client.login(email='test@user.com', password='test')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEquals(
            resp.get('Content-Disposition'),
            'attachment; filename="test.csv"'
        )
        csv_file = StringIO(resp.content.decode('utf-8'))
        reader = csv.reader(csv_file)
        csv_list = list(reader)
        self.assertEquals(len(csv_list), 5)
        self.assertEquals(len(csv_list[0]), 12)

        # question x should be in next to last column
        self.assertEquals(csv_list[0][10], "questionx")

        # old application should have blank for question x in next-to-last column
        self.assertEquals(csv_list[1][10], "")
        self.assertEquals(csv_list[1][11], "answer to last for app 1")

        # new application should have answer for question x in next-to-last column
        self.assertEquals(csv_list[4][10], "answer to questionx for app 5")
        self.assertEquals(csv_list[4][11], "answer to last for app 5")


class CoachApplicationDetailView(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        self.event = Event.objects.create(name='Test', city='Test', country='Test')
        self.page = EventPage.objects.create(event=self.event, is_live=True, url='test')
        self.form = CoachForm.objects.create(page=self.page)
        self.user = User.objects.create(email='test@user.com', is_active=True, is_staff=True)
        self.user.set_password('test')
        self.user_2 = User.objects.create(email='test2@user.com')

        self.application_1 = CoachApplication.objects.create(form=self.form, state='submitted')
        self.application_2 = CoachApplication.objects.create(form=self.form, state='accepted')
        self.application_3 = CoachApplication.objects.create(form=self.form, state='rejected')

        self.url = reverse('coaches:coach_detail', args=['test', self.application_1.id])

    def test_get_coach_application_detail(self):
        # TODO: test this
        pass
