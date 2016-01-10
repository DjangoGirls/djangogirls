import random
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from core.models import Event, EventPage, User
from coaches.models import CoachForm, CoachApplication, Question, APPLICATION_STATES, CoachEmail
from coaches.utils import DEFAULT_QUESTIONS


class CoachFormModelTest(TestCase):

    def setUp(self):
        self.event = Event.objects.create(name='Test', city='Test', country='Test')
        self.page = EventPage.objects.create(event=self.event, is_live=True, url='test')

    def test_adding_default_questions(self):
        # Each new form should automatically create default questions
        form = CoachForm.objects.create(page=self.page)
        self.assertEqual(form.question_set.count(), len(DEFAULT_QUESTIONS))

        # If you update the form, the default questions shouldn't be added
        form.text_header = 'Test'
        form.save()
        self.assertEqual(form.question_set.count(), len(DEFAULT_QUESTIONS))

    def test_number_of_applications(self):
        form = CoachForm.objects.create(page=self.page)
        self.assertEqual(form.coachapplication_set.count(), form.number_of_applications)

        CoachApplication.objects.create(form=form)
        self.assertEqual(form.coachapplication_set.count(), form.number_of_applications)
        self.assertEqual(form.coachapplication_set.count(), 1)

    def test_no_application_dates(self):
        form = CoachForm.objects.create(page=self.page)
        self.assertTrue(form.coach_application_open)

    def test_application_open(self):
        now = timezone.now()
        form = CoachForm.objects.create(page=self.page, open_from=now - timedelta(days=1),
                                        open_until=now + timedelta(days=1))
        self.assertTrue(form.coach_application_open)

    def test_application_in_future(self):
        now = timezone.now()
        form = CoachForm.objects.create(page=self.page, open_from=now + timedelta(days=1),
                                        open_until=now + timedelta(days=2))
        self.assertFalse(form.coach_application_open)

    def test_application_closed(self):
        now = timezone.now()
        form = CoachForm.objects.create(page=self.page, open_from=now - timedelta(days=2),
                                        open_until=now - timedelta(days=1))
        self.assertFalse(form.coach_application_open)


class CoachQuestionModelTest(TestCase):

    def setUp(self):
        self.event = Event.objects.create(name='Test', city='Test', country='Test')
        self.page = EventPage.objects.create(event=self.event, is_live=True, url='test')
        self.form = CoachForm.objects.create(page=self.page)

    def test_get_choices_as_list(self):
        # correctly return choices of a choices field
        question = Question.objects.filter(question_type='choices')[:1].get()
        self.assertEqual(sorted(question.get_choices_as_list()), sorted(question.choices.split(';')))

        # return TypeError if field is not a choices field
        question = Question.objects.filter(question_type='paragraph')[:1].get()
        with self.assertRaises(TypeError):
            question.get_choices_as_list()


class CoachApplicationModelTest(TestCase):

    def setUp(self):
        self.event = Event.objects.create(name='Test', city='Test', country='Test')
        self.page = EventPage.objects.create(event=self.event, is_live=True, url='test')
        self.form = CoachForm.objects.create(page=self.page)
        self.user_1 = User.objects.create(email='test@test.com')
        self.user_2 = User.objects.create(email='test2@test.com')

        self.application = CoachApplication.objects.create(form=self.form)

    def test_is_accepted(self):
        for state in APPLICATION_STATES:
            self.application.state = state[0]
            self.application.save()

            if state[0] == 'accepted':
                self.assertTrue(self.application.is_accepted)
            else:
                self.assertFalse(self.application.is_accepted)


class CoachEmailModelTest(TestCase):

    def setUp(self):
        self.event = Event.objects.create(name='Test', city='Test', country='Test')
        self.page = EventPage.objects.create(event=self.event, is_live=True, url='test')
        self.form = CoachForm.objects.create(page=self.page)
        self.application_1 = CoachApplication.objects.create(email='recipient@email.com', form=self.form, state='accepted')
        self.application_2 = CoachApplication.objects.create(email='recipient2@email.com', form=self.form, state='rejected')
        self.user = User.objects.create(email='email@email.com')

        self.email = CoachEmail.objects.create(
            form=self.form,
            author=self.user,
            subject='Test',
            text="Hey! You're awesome! Bye",
            recipients_group='accepted'
        )

    def test_send(self):
        self.email.send()
        self.assertEqual(self.email.number_of_recipients, 1)
        self.assertEqual(self.email.successfully_sent, self.application_1.email)
