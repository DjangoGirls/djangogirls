"""Tests for cron-emails sent out by the handle_emails management command."""
import mock

from click.testing import CliRunner
from django_date_extensions.fields import ApproximateDate

from django.test import TestCase
from django.utils import timezone

from applications.models import Form
from core.models import (
    Event,
    User,
)
from core.management.commands import handle_emails


class HandleEmailTestCase(TestCase):
    def setUp(self):
        self.runner = CliRunner(echo_stdin=True)

        self.sending_args = {
            'subject': 'dontcare',
            'plain_template': "emails/submit_information_email.txt",
            'html_template': "emails/submit_information_email.html",
            'timestamp_field': 'submit_information_email_sent',
            'email_type': "submit information email",
        }

    def test_approximate_date_behaviour(self):
        """ Test logic for the behaviour of skipping events with approximate dates.

            Events with approximate dates should be skipped if ignore_approximate_dates is True
        """

        # Create an event with an approximate date
        event = Event.objects.create(date=ApproximateDate(year=2017, month=1))
        self.sending_args['events'] = [event]

        with mock.patch('core.management.commands.handle_emails.send_mail') as mock_send_mail:
            # We're ignoring approximate dates, so no email should be sent
            self.sending_args['ignore_approximate_events'] = True
            handle_emails.send_event_emails(
                **self.sending_args
            )

            self.assertEqual(mock_send_mail.call_count, 0)
            mock_send_mail.reset_mock()

            # Now we're not ignoring approximate dates, so a mail should be sent.
            self.sending_args['ignore_approximate_events'] = False

            handle_emails.send_event_emails(
                **self.sending_args
            )
            self.assertEqual(mock_send_mail.call_count, 1)
            mock_send_mail.reset_mock()

            # Still ignoring approximate dates, but now the event date is fixed, so a mail should be sent.
            event.date = timezone.datetime.now()
            event.save()

            handle_emails.send_event_emails(
                **self.sending_args
            )
            self.assertEqual(mock_send_mail.call_count, 1)
            mock_send_mail.reset_mock()

    def test_email_recipients(self):
        """ All emails should go to event.email and all team members, but only once. """
        event = Event.objects.create(email='user-1@example.com')
        self.sending_args['events'] = [event]

        for x in range(2):
            user = User.objects.create(email='user-{}@example.com'.format(x))
            event.team.add(user)

        with mock.patch('core.management.commands.handle_emails.send_mail') as mock_send_mail:
            handle_emails.send_event_emails(
                **self.sending_args
            )
            _, send_kwargs = mock_send_mail.call_args

            self.assertCountEqual(send_kwargs['recipient_list'], ['user-0@example.com', 'user-1@example.com'])

    def test_email_template_rendering(self):
        """ Test basic email rendering for templates and content. """
        city_name = "definitely not a city that will actually show up in a template"
        event = Event.objects.create(city=city_name, email='user-1@example.com')
        self.sending_args['events'] = [event]

        self.sending_args['subject'] = "testing {{event.city}} {{event.email}}"

        with mock.patch('core.management.commands.handle_emails.send_mail') as mock_send_mail:
            handle_emails.send_event_emails(
                **self.sending_args
            )
            _, send_kwargs = mock_send_mail.call_args

            self.assertEqual(mock_send_mail.call_count, 1)
            self.assertIn("<p>", send_kwargs['html_message'])
            self.assertNotIn("<p>", send_kwargs['message'])
            self.assertEqual("testing {} {}".format(event.city, event.email), send_kwargs['subject'])
            self.assertTrue(event.city in send_kwargs['html_message'])

    def test_thank_you_email_logic(self):
        """ Test event filtering logic for thank you emails. """
        should_be_included = Event.objects.create(
            city="should be included",
            is_on_homepage=True,
            date=timezone.now() - timezone.timedelta(days=1),
        )
        Event.objects.create(
            city="not on homepage",
            is_on_homepage=False,
            date=timezone.now() - timezone.timedelta(days=1),
        )
        Event.objects.create(
            city="in future",
            is_on_homepage=True,
            date=timezone.now() + timezone.timedelta(days=1),
        )
        Event.objects.create(
            city="already sent",
            is_on_homepage=True,
            date=timezone.now() - timezone.timedelta(days=1),
            thank_you_email_sent=timezone.now()
        )

        with mock.patch('core.management.commands.handle_emails.send_mail') as mock_send_mail:
            handle_emails.send_thank_you_emails()

            # Only a single event should have been picked up
            self.assertEqual(mock_send_mail.call_count, 1)
            _, send_kwargs = mock_send_mail.call_args
            self.assertIn(should_be_included.city, send_kwargs['subject'])

    def test_submit_information_email_logic(self):
        """ Test event filtering logic for thank you emails. """
        eight_weeks_ago = timezone.now() - timezone.timedelta(weeks=8)

        should_be_included = Event.objects.create(
            city="should be included",
            is_on_homepage=True,
            date=eight_weeks_ago
        )
        Event.objects.create(
            city="not on homepage",
            is_on_homepage=False,
            date=eight_weeks_ago
        )
        Event.objects.create(
            city="uncertain date",
            is_on_homepage=True,
            date=ApproximateDate(year=eight_weeks_ago.year, month=eight_weeks_ago.month)
        )
        Event.objects.create(
            city="data already provided",
            is_on_homepage=True,
            date=eight_weeks_ago,
            applicants_count=1,
            attendees_count=1
        )
        Event.objects.create(
            city="already sent",
            is_on_homepage=True,
            date=eight_weeks_ago,
            submit_information_email_sent=timezone.now()
        )

        with mock.patch('core.management.commands.handle_emails.send_mail') as mock_send_mail:
            handle_emails.send_submit_information_emails()

            # Only a single event should have been picked up
            self.assertEqual(mock_send_mail.call_count, 1)
            _, send_kwargs = mock_send_mail.call_args
            self.assertIn(should_be_included.city, send_kwargs['subject'])

    def test_offer_help_email_form_logic(self):
        """ Test event filtering logic for thank you emails depending on their application form. """
        now = timezone.now()
        in_six_weeks = now + timezone.timedelta(weeks=6)

        @mock.patch('core.management.commands.handle_emails.send_mail')
        def _would_send_email(event, mock_send_mail):
            """ Return true if given event would currently trigger an "offer help" email. """
            handle_emails.send_offer_help_emails()

            if mock_send_mail.call_count == 0:
                return False

            _, send_kwargs = mock_send_mail.call_args
            mock_send_mail.reset_mock()

            return event.city in send_kwargs['subject']

        # Test one event with no form, should send an email
        event = Event.objects.create(
            city="Test City",
            is_on_homepage=True,
            date=in_six_weeks,
            is_page_live=True
        )
        self.assertTrue(_would_send_email(event))

        # Event with a rough date at least a month in the future should also send an email
        event.date = ApproximateDate(year=in_six_weeks.year, month=in_six_weeks.month)
        event.save()
        self.assertTrue(_would_send_email(event))

        # Event with a start date in the past shouldn't trigger an email
        event.date = now - timezone.timedelta(days=1)
        event.save()
        self.assertFalse(_would_send_email(event))

        # Nor should an event with an uncertain date in the current month.
        event.date = ApproximateDate(year=now.year, month=now.month)
        event.save()
        self.assertFalse(_would_send_email(event))

        # Event now has a form that is still open, which should trigger an email
        event.date = in_six_weeks
        event.save()
        Form.objects.create(event=event, open_until=now + timezone.timedelta(days=1))
        self.assertTrue(_would_send_email(event))

        # The form is now closed, no email should be sent.
        event.form.open_until = now - timezone.timedelta(days=1)
        event.form.save()
        self.assertFalse(_would_send_email(event))

        # Set page to not live, email should be sent again
        event.is_page_live = False
        event.save()
        self.assertTrue(_would_send_email(event))

        # Remove from homepage, no email should be sent.
        event.is_on_homepage = False
        event.save()
        self.assertFalse(_would_send_email(event))
