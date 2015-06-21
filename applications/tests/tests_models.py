import random
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from core.models import Event, EventPage, User
from applications.models import Form, Application, Question, Score, APPLICATION_STATES, Email
from applications.utils import DEFAULT_QUESTIONS


class FormModel(TestCase):

    def setUp(self):
        self.event = Event.objects.create(name='Test', city='Test', country='Test')
        self.page = EventPage.objects.create(event=self.event, is_live=True, url='test')

    def test_adding_default_questions(self):
        # Each new form should automatically create default questions
        form = Form.objects.create(page=self.page)
        self.assertEqual(form.question_set.count(), len(DEFAULT_QUESTIONS))

        # If you update the form, the default questions shouldn't be added
        form.text_header = 'Test'
        form.save()
        self.assertEqual(form.question_set.count(), len(DEFAULT_QUESTIONS))

    def test_number_of_applications(self):
        form = Form.objects.create(page=self.page)
        self.assertEqual(form.application_set.count(), form.number_of_applications)

        Application.objects.create(form=form)
        self.assertEqual(form.application_set.count(), form.number_of_applications)
        self.assertEqual(form.application_set.count(), 1)

    def test_no_application_dates(self):
        form = Form.objects.create(page=self.page)
        self.assertTrue(form.application_open)

    def test_application_open(self):
        now = timezone.now()
        form = Form.objects.create(page=self.page, open_from=now - timedelta(days=1),
                                   open_until=now + timedelta(days=1))
        self.assertTrue(form.application_open)

    def test_application_in_future(self):
        now = timezone.now()
        form = Form.objects.create(page=self.page, open_from=now + timedelta(days=1),
                                   open_until=now + timedelta(days=2))
        self.assertFalse(form.application_open)

    def test_application_closed(self):
        now = timezone.now()
        form = Form.objects.create(page=self.page, open_from=now - timedelta(days=2),
                                   open_until=now - timedelta(days=1))
        self.assertFalse(form.application_open)


class QuestionModel(TestCase):

    def setUp(self):
        self.event = Event.objects.create(name='Test', city='Test', country='Test')
        self.page = EventPage.objects.create(event=self.event, is_live=True, url='test')
        self.form = Form.objects.create(page=self.page)

    def test_get_choices_as_list(self):
        # correctly return choices of a choices field
        question = Question.objects.filter(question_type='choices')[:1].get()
        self.assertEqual(sorted(question.get_choices_as_list()), sorted(question.choices.split(';')))

        # return TypeError if field is not a choices field
        question = Question.objects.filter(question_type='paragraph')[:1].get()
        with self.assertRaises(TypeError):
            question.get_choices_as_list()


class ApplicationModel(TestCase):

    def setUp(self):
        self.event = Event.objects.create(name='Test', city='Test', country='Test')
        self.page = EventPage.objects.create(event=self.event, is_live=True, url='test')
        self.form = Form.objects.create(page=self.page)
        self.user_1 = User.objects.create(email='test@test.com')
        self.user_2 = User.objects.create(email='test2@test.com')

        self.application = Application.objects.create(form=self.form)

    def test_average_score(self):
        self.assertEqual(self.application.average_score, 0)

        score_1 = Score.objects.create(user=self.user_1, application=self.application, score=random.randint(0,5))
        score_2 = Score.objects.create(user=self.user_2, application=self.application, score=random.randint(0,5))
        average = sum([score_1.score, score_2.score]) / 2.0

        self.assertEqual(self.application.average_score, average)

    def test_generating_code(self):
        self.assertEqual(len(self.application.generate_code()), 24)

    def test_get_rsvp_yes_code(self):
        self.assertIsNone(self.application.rsvp_yes_code)
        rsvp_code = self.application.get_rsvp_yes_code()
        self.assertEqual(len(rsvp_code), 24)
        self.assertEqual(self.application.rsvp_yes_code, rsvp_code)

        # Make sure it doesn't generate again:
        self.assertEqual(self.application.get_rsvp_yes_code(), rsvp_code)

    def test_get_rsvp_no_code(self):
        self.assertIsNone(self.application.rsvp_no_code)
        rsvp_code = self.application.get_rsvp_no_code()
        self.assertEqual(len(rsvp_code), 24)
        self.assertEqual(self.application.rsvp_no_code, rsvp_code)

        # Make sure it doesn't generate again:
        self.assertEqual(self.application.get_rsvp_no_code(), rsvp_code)

    def test_get_by_rsvp_code(self):
        rsvp_code_no = self.application.get_rsvp_no_code()
        rsvp_code_yes = self.application.get_rsvp_yes_code()

        self.assertEqual(Application.get_by_rsvp_code(rsvp_code_yes, self.page), (self.application, 'yes'))
        self.assertEqual(Application.get_by_rsvp_code(rsvp_code_no, self.page), (self.application, 'no'))
        self.assertIsNone(Application.get_by_rsvp_code('notexisting', self.page))

    def test_is_accepted(self):
        for state in APPLICATION_STATES:
            self.application.state = state[0]
            self.application.save()

            if state[0] == 'accepted':
                self.assertTrue(self.application.is_accepted)
            else:
                self.assertFalse(self.application.is_accepted)


class EmailModel(TestCase):

    def setUp(self):
        self.event = Event.objects.create(name='Test', city='Test', country='Test')
        self.page = EventPage.objects.create(event=self.event, is_live=True, url='test')
        self.form = Form.objects.create(page=self.page)
        self.application = Application.objects.create(email='recipient@email.com', form=self.form, state='accepted')
        self.user = User.objects.create(email='email@email.com')

        self.email = Email.objects.create(
            form=self.form,
            author=self.user,
            subject='Test',
            text='Hey! [rsvp-url-yes] [rsvp-url-no] Bye',
            recipients_group='accepted'
        )

    def test_get_rsvp_link(self):
        link = self.email.get_rsvp_link('abcd')
        self.assertIn('abcd', link)
        self.assertIn(self.page.url, link)

    def test_add_rsvp_links(self):
        self.assertIn('[rsvp-url-yes]', self.email.text)
        self.assertIn('[rsvp-url-no]', self.email.text)
        body = self.email.add_rsvp_links(self.email.text, self.application)
        self.assertIn(self.application.get_rsvp_yes_code(), body)
        self.assertIn(self.application.get_rsvp_no_code(), body)
        self.assertNotIn('[rsvp-url-yes]', body)
        self.assertNotIn('[rsvp-url-no]', body)

    def test_send(self):
        self.email.send()
        self.assertEqual(self.email.number_of_recipients, 1)
        self.assertEqual(self.email.successfuly_sent, self.application.email)
