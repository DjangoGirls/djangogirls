import csv
import json
from datetime import timedelta
from io import StringIO

from django.test import RequestFactory, TestCase
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from applications.models import (RSVP_NO, RSVP_WAITING, RSVP_YES, Answer,
                                 Application, Form, Question, Score)
from applications.utils import DEFAULT_QUESTIONS
from applications.views import application_list
from core.models import Event, User


class ApplyView(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        self.event = Event.objects.create(
            name='Test', city='Test', country='Test',
            is_page_live=True, page_url='test')
        self.form = Form.objects.create(event=self.event)

    def test_access_apply_view(self):
        resp = self.client.get(reverse('applications:apply', args=['test']))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['form_obj'], self.form)
        # there is two more fields than default questions,
        # because we always add newsletter option at the end and a captcha
        self.assertEqual(
            len(resp.context['form'].fields), len(DEFAULT_QUESTIONS) + 2)

        # Redirect to event page because there is no form
        self.form.delete()
        resp = self.client.get(reverse('applications:apply', args=['test']))
        self.assertEqual(resp.status_code, 302)

        # Show 404 because there is no event page
        self.event.delete()
        resp = self.client.get(reverse('applications:apply', args=['test']))
        self.assertEqual(resp.status_code, 404)

    def test_application_not_open(self):
        now = timezone.now()
        self.form.open_from = now + timedelta(days=1)
        self.form.open_until = now + timedelta(days=2)
        self.form.save()

        resp = self.client.get(reverse('applications:apply', args=['test']))
        self.assertEqual(resp.status_code, 302)

    def test_application_open(self):
        now = timezone.now()
        self.form.open_from = now - timedelta(days=1)
        self.form.open_until = now + timedelta(days=1)
        self.form.save()

        resp = self.client.get(reverse('applications:apply', args=['test']))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['form_obj'], self.form)

    def test_application_not_open_organiser(self):
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

        resp = self.client.get(reverse('applications:apply', args=['test']))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['form_obj'], self.form)

    def test_application_not_open_super_user(self):
        now = timezone.now()
        self.form.open_from = now + timedelta(days=1)
        self.form.open_until = now + timedelta(days=2)
        self.form.save()

        user = User.objects.create(
            email='test@user.com', is_active=True, is_staff=True, is_superuser=True)
        user.set_password('test')
        user.save()
        self.client.login(email='test@user.com', password='test')

        resp = self.client.get(reverse('applications:apply', args=['test']))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['form_obj'], self.form)


class ApplicationsView(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        self.event = Event.objects.create(
            name='Test', city='Test', country='Test',
            is_page_live=True, page_url='test')
        self.event2 = Event.objects.create(
            name='Test 2', city='Test 2', country='Test 2',
            is_page_live=True, page_url='test2')
        self.form = Form.objects.create(event=self.event)
        self.form_2 = Form.objects.create(event=self.event2)
        self.user = User.objects.create(
            email='test@user.com', is_active=True, is_staff=True)
        self.user.set_password('test')
        self.user_2 = User.objects.create(email='test2@user.com')

        self.application_1 = Application.objects.create(
            form=self.form, state='submitted')
        self.application_2 = Application.objects.create(
            form=self.form, state='accepted')
        self.application_3 = Application.objects.create(
            form=self.form, state='rejected')
        self.application_4 = Application.objects.create(
            form=self.form, state='waitlisted')

        self.url = reverse('applications:applications', args=['test'])

    def test_access_applications_view(self):
        # as anonymous user
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

        # as logged in user, but not orgarniser of given event
        request = self.factory.get(self.url)
        request.user = self.user
        resp = application_list(request, city='test')
        self.assertEqual(resp.status_code, 404)

        # as superuser
        self.user.is_superuser = True
        self.user.save()
        request = self.factory.get(self.url)
        request.user = self.user
        resp = application_list(request, city='test')
        self.assertEqual(resp.status_code, 200)

        # as organiser of given event
        self.user.is_superuser = False
        self.user.save()
        self.event.team.add(self.user)
        self.event.save()
        request = self.factory.get(self.url)
        request.user = self.user
        resp = application_list(request, city='test')
        self.assertEqual(resp.status_code, 200)

    def test_organiser_only_decorator_without_city(self):
        request = self.factory.get('')
        request.user = self.user
        with self.assertRaises(ValueError):
            application_list(request, city=None)

    def test_get_applications_list(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.login(email='test@user.com', password='test')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['applications']), 4)

        # change one application's form
        self.application_1.form = self.form_2
        self.application_1.save()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['applications']), 3)

    def test_organiser_menu_in_applications_list(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.login(email='test@user.com', password='test')
        resp = self.client.get(self.url)
        self.assertContains(
            resp,
            '<li><a href="/test/applications/">Applications</a></li>',
            html=True,
        )
        self.assertContains(
            resp,
            '<li><a href="/test/communication/">Messaging</a></li>',
            html=True,
        )

    def test_get_sorted_applications_list(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.login(email='test@user.com', password='test')

        # Add some scores:
        Score.objects.create(application=self.application_1,
                             user=self.user, score=2.0)
        Score.objects.create(application=self.application_1,
                             user=self.user_2, score=4.0)
        Score.objects.create(application=self.application_2,
                             user=self.user, score=3.0)
        Score.objects.create(application=self.application_2,
                             user=self.user_2, score=3.0)
        Score.objects.create(application=self.application_3,
                             user=self.user, score=3.0)
        Score.objects.create(application=self.application_3,
                             user=self.user_2, score=4.0)

        # Order by average_score
        resp = self.client.get('{}?order=average_score'.format(self.url))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['applications']), 4)
        self.assertEqual(
            resp.context['applications'],
            [self.application_4, self.application_1, self.application_2,
             self.application_3]
        )
        self.assertEqual(resp.context['order'], 'average_score')

        # Order by -average_score
        resp = self.client.get('{}?order=-average_score'.format(self.url))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['applications']), 4)
        self.assertEqual(
            resp.context['applications'],
            [self.application_3, self.application_2, self.application_1,
             self.application_4]
        )
        self.assertEqual(resp.context['order'], '-average_score')

    def get_filtered_applications_list(self):
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

        # Filter by wait listed
        resp.self.client.get('{}?state=waitlisted'.format(self.url))
        self.assertEqual(len(resp.context['applications']), 1)
        self.assertEqual(resp.context['applications'], [self.application_4])

    def test_changing_application_status(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.login(email='test@user.com', password='test')

        self.assertEqual(self.application_1.state, 'submitted')
        resp = self.client.post(
            reverse('applications:change_state', args=['test']),
            {'state': 'accepted', 'application': self.application_1.id}
        )
        self.assertEqual(resp.status_code, 200)
        self.application_1 = Application.objects.get(id=self.application_1.id)
        self.assertEqual(self.application_1.state, 'accepted')

    def test_yes_rsvp(self):
        self.assertEqual(self.application_2.rsvp_status, RSVP_WAITING)
        args = ['test', self.application_2.get_rsvp_yes_code()]
        resp = self.client.get(
            reverse('applications:rsvp', args=args)
        )
        self.assertEqual(resp.status_code, 200)
        self.application_2 = Application.objects.get(id=self.application_2.id)
        self.assertEqual(self.application_2.rsvp_status, RSVP_YES)

    def test_repeated_rsvp(self):
        self.application_2.rsvp_status = RSVP_YES
        self.application_2.save()
        self.assertEqual(self.application_2.rsvp_status, RSVP_YES)
        args = ['test', self.application_2.get_rsvp_no_code()]
        resp = self.client.get(
            reverse('applications:rsvp', args=args)
        )
        self.assertEqual(resp.status_code, 302)
        self.application_2 = Application.objects.get(id=self.application_2.id)
        self.assertEqual(self.application_2.rsvp_status, RSVP_YES)

    def test_no_rsvp(self):
        self.application_2.rsvp_status = RSVP_WAITING
        self.application_2.save()
        self.assertEqual(self.application_2.rsvp_status, RSVP_WAITING)
        args = ['test', self.application_2.get_rsvp_no_code()]
        resp = self.client.get(
            reverse('applications:rsvp', args=args)
        )
        self.assertEqual(resp.status_code, 200)
        self.application_2 = Application.objects.get(id=self.application_2.id)
        self.assertEqual(self.application_2.rsvp_status, RSVP_NO)

    def test_nonexistent_rsvp(self):
        self.assertEqual(self.application_2.rsvp_status, RSVP_WAITING)
        args = ['test', 'sssss']
        resp = self.client.get(
            reverse('applications:rsvp', args=args)
        )
        self.assertEqual(resp.status_code, 302)
        self.application_2 = Application.objects.get(id=self.application_2.id)
        self.assertEqual(self.application_2.rsvp_status, RSVP_WAITING)

    def test_changing_application_rsvp(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.login(email='test@user.com', password='test')

        self.assertEqual(self.application_1.rsvp_status, RSVP_WAITING)
        resp = self.client.post(
            reverse('applications:change_rsvp', args=['test']),
            {'rsvp_status': RSVP_YES, 'application': self.application_1.id}
        )
        self.assertEqual(resp.status_code, 200)
        self.application_1 = Application.objects.get(id=self.application_1.id)
        self.assertEqual(self.application_1.rsvp_status, RSVP_YES)

    def test_changing_application_status_errors(self):
        # user without permissions:
        resp = self.client.post(
            reverse('applications:change_state', args=['test']),
            {'state': 'accepted', 'application': self.application_1.id}
        )
        self.assertEqual(resp.status_code, 302)

        self.user.is_superuser = True
        self.user.save()
        self.client.login(email='test@user.com', password='test')

        # lack of state parameter
        resp = self.client.post(
            reverse('applications:change_state', args=['test']),
            {'application': self.application_1.id}
        )
        self.assertTrue('error' in json.loads(resp.content.decode('utf-8')))

        # lack of application parameter
        resp = self.client.post(
            reverse('applications:change_state', args=['test']),
            {'state': 'accepted'}
        )
        self.assertTrue('error' in json.loads(resp.content.decode('utf-8')))

    def test_changing_application_rsvp_errors(self):
        # user without permissions:
        resp = self.client.post(
            reverse('applications:change_rsvp', args=['test']),
            {'rsvp_status': RSVP_YES, 'application': self.application_1.id}
        )
        self.assertEqual(resp.status_code, 302)

        self.user.is_superuser = True
        self.user.save()
        self.client.login(email='test@user.com', password='test')

        # lack of rsvp_status parameter
        resp = self.client.post(
            reverse('applications:change_rsvp', args=['test']),
            {'application': self.application_1.id}
        )
        self.assertTrue('error' in json.loads(resp.content.decode('utf-8')))

        # lack of application parameter
        resp = self.client.post(
            reverse('applications:change_rsvp', args=['test']),
            {'rsvp_status': RSVP_YES}
        )
        self.assertTrue('error' in json.loads(resp.content.decode('utf-8')))

    def changing_application_status_in_bulk(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.login(email='test@user.com', password='test')

        self.assertEqual(self.application_1.state, 'submitted')
        self.assertEqual(self.application_3.state, 'rejected')
        resp = self.client.post(
            reverse('applications:change_state', args=['test']),
            {'state': 'accepted', 'application': [
                self.application_1.id, self.application_3.id]}
        )
        self.assertEqual(resp.status_code, 200)
        self.application_1 = Application.objects.get(id=self.application_1.id)
        self.application_3 = Application.objects.get(id=self.application_3.id)
        self.assertEqual(self.application_1.state, 'accepted')
        self.assertEqual(self.application_3.state, 'accepted')


class ApplicationsDownloadView(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        self.event = Event.objects.create(
            name='Test', city='Test', country='Test',
            is_page_live=True, page_url='test')
        self.form = Form.objects.create(event=self.event)

        self.user = User.objects.create(
            email='test@user.com', is_active=True, is_staff=True)
        self.user.set_password('test')

        self.application_1 = Application.objects.create(
            form=self.form, state='submitted')
        self.application_2 = Application.objects.create(
            form=self.form, state='accepted')
        self.application_3 = Application.objects.create(
            form=self.form, state='rejected')
        self.application_4 = Application.objects.create(
            form=self.form, state='waitlisted')

        self.last_question = self.form.question_set.last()
        self.application_1_last_answer = Answer.objects.create(
            application=self.application_1, question=self.last_question, answer='answer to last for app 1')

        self.url = reverse('applications:applications_csv', args=['test'])

    def test_download_applications_list(self):
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
        self.assertEquals(len(csv_list[0]), 18)
        self.assertEquals(csv_list[0][0], "Application Number")
        self.assertEquals(csv_list[1][1], "submitted")
        self.assertEquals(csv_list[2][1], "accepted")
        self.assertEquals(csv_list[3][1], "rejected")
        self.assertEquals(csv_list[4][1], "waitlisted")
        self.assertEquals(csv_list[1][17], "answer to last for app 1")

    def test_download_applications_list_uses_query_parameters_to_filter_applications(self):
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

    def test_download_applications_list_with_question_added(self):

        # add new question x as next to last question
        self.question_x = Question.objects.create(
            form=self.form, question_type='text', order=self.last_question.order, title='questionx')
        self.last_question.order = self.last_question.order + 1
        self.last_question.save()

        # now create a new application with answer to the new question
        self.application_5 = Application.objects.create(
            form=self.form, state='submitted')
        self.application_5_x_answer = Answer.objects.create(
            application=self.application_5, question=self.question_x, answer='answer to questionx for app 5')
        self.application_5_last_answer = Answer.objects.create(
            application=self.application_5, question=self.last_question, answer='answer to last for app 5')

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
        self.assertEquals(len(csv_list), 6)
        self.assertEquals(len(csv_list[0]), 19)

        # question x should be in next to last column
        self.assertEquals(csv_list[0][17], "questionx")

        # old application should have blank for question x in next-to-last
        # column
        self.assertEquals(csv_list[1][17], "")
        self.assertEquals(csv_list[1][18], "answer to last for app 1")

        # new application should have answer for question x in next-to-last
        # column
        self.assertEquals(csv_list[5][17], "answer to questionx for app 5")
        self.assertEquals(csv_list[5][18], "answer to last for app 5")
