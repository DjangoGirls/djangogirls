import time
from datetime import timedelta, datetime

from django.test import TestCase
from django.utils import timezone

from model_mommy import mommy

from jobs.models import Job, Meetup


class JobModelTests(TestCase):
    """Tests for custom methods of Job model."""

    def setUp(self):
        """Setting up models with mommy."""
        self.job = mommy.make(Job, ready_to_publish=True)
        self.job1 = mommy.make(Job, ready_to_publish=False)

    def test_publish_succesfully(self):
        """Plain publish method test without any twists."""
        self.assertFalse(self.job.published_date)
        self.job.publish()
        self.assertTrue(self.job.published_date, "Job has no published date.")

    def test_publish_unsuccesfully(self):
        """Publish doesn't work when ready_to_publish field is set to False."""
        self.assertFalse(self.job1.published_date)
        self.job1.publish()
        self.assertFalse(self.job1.published_date, "Job has published date.")

    def test_publish_more_than_once_and_change_values(self):
        """Publish once, than change ready_to_publish field value,
        publish once more."""
        self.assertFalse(self.job.published_date)
        self.job.publish()
        self.job.ready_to_publish = False
        # Right now if we change ready_to_publish to False,
        # published_date stays as it was and doesn't become None.
        self.assertTrue(self.job.published_date)
        self.job.ready_to_publish = True
        self.job.publish()
        self.assertTrue(self.job.published_date, "Job has no published date.")

    def test_publish_twice_in_a_row(self):
        """Publish twice in a row
        - every time new published date is being created"""
        self.assertFalse(self.job.published_date)
        self.job.publish()
        first_date = self.job.published_date
        self.job.publish()
        second_date = self.job.published_date
        self.assertTrue(self.job.published_date, "Job has no published date.")
        self.assertNotEqual(first_date, second_date)

    #TODO
    def test_publish_without_review(self):
        """Job may be published without review -
        possibly not something we want to be done."""
        self.assertFalse(self.job.review_status, "Job was already reviewed.")
        self.job.publish()
        self.assertTrue(self.job.published_date, "Job has no published date.")

    def test_expiration_date_default_value(self):
        """Test if default value is 60 days from now."""
        self.job.publish()
        self.assertFalse(self.job.expiration_date)
        self.job.set_expiration_date()
        result = self.job.expiration_date - timezone.now()
        self.assertEqual(result.days, 59)

    def test_expiration_date_on_not_ready(self):
        """Test setting expiration date if job is unpublished."""
        value = self.job.set_expiration_date()
        self.assertEqual(value, None)
        self.assertFalse(self.job.expiration_date)

    def test_set_expiration_date_twice(self):
        """Test setting expiration date more than once in a row."""
        self.job.publish()
        self.assertFalse(self.job.expiration_date)
        self.job.set_expiration_date()
        first_date = self.job.expiration_date
        self.assertTrue(self.job.expiration_date, "Job has no expiration date.")
        self.job.publish()
        self.job.set_expiration_date()
        second_date = self.job.expiration_date
        self.assertTrue(self.job.expiration_date, "Job has no expiration date.")
        self.assertTrue(second_date.second > first_date.second)


class MeetupModelTests(TestCase):
    """Tests for custom methods of Meetup model."""

    def test_publish_without_ready_to_publish(self):
        """Trying to publish meetups which are not ready to publish
        should results in an assertion error"""
        meetup_not_ready = Meetup(ready_to_publish=False)
        self.assertRaises(AssertionError,  meetup_not_ready.publish)

    def test_publish_with_default_expiration_date(self):
        """Testing the publish method with no expiration date set"""
        meetup_ready_no_exp_date = Meetup(
            ready_to_publish=True,
            expiration_date=None
        )
        meetup_ready_no_exp_date.publish()
        self.assertTrue(meetup_ready_no_exp_date.published_date)
        self.assertAlmostEqual(
            meetup_ready_no_exp_date.published_date,
            timezone.now(),
            delta=timedelta(seconds=10)
        )
        self.assertTrue(meetup_ready_no_exp_date.expiration_date)
        result = meetup_ready_no_exp_date.expiration_date - timezone.now()
        self.assertEqual(result.days, 59)

    def test_publish_with_custom_expiration_date(self):
        """Testing the publish method with custom expiration date set"""
        custom_date = datetime(2016, 2, 14, 15, 30)
        meetup_ready_custom_exp_date = Meetup(
            ready_to_publish=True,
            expiration_date=custom_date
        )
        meetup_ready_custom_exp_date.publish()
        self.assertEqual(
            meetup_ready_custom_exp_date.expiration_date,
            custom_date
        )
