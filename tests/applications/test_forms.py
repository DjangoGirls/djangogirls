import pytest
import vcr

from applications.forms import ApplicationForm
from applications.models import Application, Form, Question
from core.models import Event


@pytest.mark.django_db
@vcr.use_cassette('tests/applications/vcr/application_form_prevent_duplicate_emails.yaml')
def test_application_form_prevent_duplicate_emails():
    event = Event.objects.create(
        name='Test', city='Test', country='Test',
        is_page_live=True, page_url='test')
    form = Form.objects.create(event=event)

    # Override default questions, we need just the e-mail
    form.question_set.all().delete()
    question = Question.objects.create(
        title="Your e-mail address:",
        question_type="email",
        form=form,
        order=1)

    assert Application.objects.count() == 0

    form_data = {
        'newsletter_optin': 'yes',
        'g-recaptcha-response': 'PASSED',
        'question_{}'.format(question.pk): 'test@test.pl'
    }

    application_form = ApplicationForm(form_data, form=form)
    assert application_form.is_valid()

    application_form.save()
    assert Application.objects.count() == 1

    application_form = ApplicationForm(form_data, form=form)
    assert not application_form.is_valid()
