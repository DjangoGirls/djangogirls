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
        self.custom_date = datetime(2016, 2, 14, 15, 30, tzinfo=timezone.utc)
        self.job_not_ready = mommy.make(Job, ready_to_publish=False)
        self.job_ready_no_exp_date = mommy.make(
            Job,
            ready_to_publish=True,
            expiration_date=None
        )
        self.job_ready_custom_exp_date = mommy.make(
            Job,
            ready_to_publish=True,
            expiration_date=self.custom_date
        )

    def test_publish_without_ready_to_publish(self):
        """Attempts to publish jobs with ready_to_published=False
        should results in an assertion error"""
        self.assertRaises(AssertionError,  self.job_not_ready.publish)

    def test_expiration_date_default_value(self):
        """Tests if default value is 60 days from now."""
        self.job_ready_no_exp_date.publish()
        self.assertTrue(self.job_ready_no_exp_date.published_date)
        self.assertAlmostEqual(
            self.job_ready_no_exp_date.published_date,
            timezone.now(),
            delta=timedelta(seconds=10)
        )
        self.assertTrue(self.job_ready_no_exp_date.expiration_date)
        result = self.job_ready_no_exp_date.expiration_date - timezone.now()
        self.assertEqual(result.days, 59)

    def test_publish_with_custom_expiration_date(self):
        """Tests the publish method with custom expiration date set"""
        self.job_ready_custom_exp_date.publish()
        self.assertEqual(
            self.job_ready_custom_exp_date.expiration_date,
            self.custom_date
        )

    def test_publish_twice_in_a_row(self):
        """Publish twice in a row
        - every time new published date is being created"""
        self.assertFalse(self.job_ready_no_exp_date.published_date)
        self.job_ready_no_exp_date.publish()
        first_date = self.job_ready_no_exp_date.published_date
        self.job_ready_no_exp_date.publish()
        second_date = self.job_ready_no_exp_date.published_date
        self.assertTrue(self.job_ready_no_exp_date.published_date, "Job has no published date.")
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

    def setUp(self):
        """Setting up models with mommy."""
        self.custom_date = datetime(2016, 2, 14, 15, 30, tzinfo=timezone.utc)
        self.meetup_not_ready = mommy.make(Meetup, ready_to_publish=False)
        self.meetup_ready_no_exp_date = mommy.make(
            Meetup,
            ready_to_publish=True,
            expiration_date=None
        )
        self.meetup_ready_custom_exp_date = mommy.make(
            Meetup,
            ready_to_publish=True,
            expiration_date=self.custom_date
        )

    def test_publish_without_ready_to_publish(self):
        """Attempts to publish meetups with ready_to_published=False
        should results in an assertion error"""
        self.assertRaises(AssertionError,  self.meetup_not_ready.publish)

    def test_publish_with_default_expiration_date(self):
        """Tests the publish method with no expiration date set"""
        self.meetup_ready_no_exp_date.publish()
        self.assertTrue(self.meetup_ready_no_exp_date.published_date)
        self.assertAlmostEqual(
            self.meetup_ready_no_exp_date.published_date,
            timezone.now(),
            delta=timedelta(seconds=10)
        )
        self.assertTrue(self.meetup_ready_no_exp_date.expiration_date)
        result = self.meetup_ready_no_exp_date.expiration_date - timezone.now()
        self.assertEqual(result.days, 59)

    def test_publish_with_custom_expiration_date(self):
        """Tests the publish method with custom expiration date set"""
        self.meetup_ready_custom_exp_date.publish()
        self.assertEqual(
            self.meetup_ready_custom_exp_date.expiration_date,
            self.custom_date
        )
