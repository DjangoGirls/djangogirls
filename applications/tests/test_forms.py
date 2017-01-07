import os

import vcr
from django.test import TestCase

from applications.forms import ApplicationForm
from applications.models import Application, Form, Question
from core.models import Event


class MenuTest(TestCase):

    def setUp(self):
        self.event = Event.objects.create(
            name='Test', city='Test', country='Test',
            is_page_live=True, page_url='test')
        self.form = Form.objects.create(event=self.event)

        os.environ['RECAPTCHA_TESTING'] = 'True'

    @vcr.use_cassette('applications/tests/vcr/application_form_prevent_duplicate_emails.yaml')
    def test_application_form_prevent_duplicate_emails(self):
        form_questions = [
            {
                "title": "Your e-mail address:",
                "question_type": "email",
            }
        ]
        # Override default questions, we need just the e-mail
        self.form.question_set.all().delete()
        for i, question in enumerate(form_questions, start=1):
            question['form'] = self.form
            question['order'] = i
            Question.objects.create(**question)

        self.assertEqual(Application.objects.count(), 0)
        questions = self.form.question_set.all()

        form_data = {
            'newsletter_optin': 'yes',
            'g-recaptcha-response': 'PASSED'
        }
        for question in questions:
            if question.title == "Your e-mail address:":
                form_data.update({
                    'question_{}'.format(question.pk): 'test@test.pl'
                })
                continue

        form = ApplicationForm(form_data, form=self.form)

        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(Application.objects.count(), 1)
        form = ApplicationForm(form_data, form=self.form)
        self.assertFalse(form.is_valid())

    def tearDown(self):
        os.environ['RECAPTCHA_TESTING'] = 'False'
