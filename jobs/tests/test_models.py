from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from model_mommy import mommy

from jobs.models import Job, Meetup


class JobModelTests(TestCase):
    """Tests for custom methods of Job model."""

    def setUp(self):
        """Setting up models with mommy."""
        self.custom_date = timezone.now() + timedelta(days=45)
        self.job_not_ready = mommy.make(Job, review_status=Job.OPEN)
        self.job_ready_no_exp_date = mommy.make(
            Job,
            review_status=Job.READY_TO_PUBLISH,
            expiration_date=None
        )
        self.job_ready_custom_exp_date = mommy.make(
            Job,
            review_status=Job.READY_TO_PUBLISH,
            expiration_date=self.custom_date
        )

    def test_is_ready_to_publish_for_not_ready(self):
        """Tests if the is_ready_to_publish_method returns correct value
        for a job not ready to publish"""
        self.assertFalse(self.job_not_ready.is_ready_to_publish())

    def test_is_ready_to_publish_for_ready(self):
        """Tests if the is_ready_to_publish_method returns correct value
        for a job ready to publish"""
        self.assertTrue(self.job_ready_no_exp_date.is_ready_to_publish())

    def test_publish_not_ready_to_publish(self):
        """Attempts to publish jobs which are not in the READY_TO_PUBLISH state,
        it should results in an assertion error"""
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
        """It is not possible to publish a job offer twice"""
        self.assertFalse(self.job_ready_no_exp_date.published_date)
        self.job_ready_no_exp_date.publish()
        self.assertTrue(self.job_ready_no_exp_date.published_date, "Job has no published date.")
        self.assertRaises(AssertionError, self.job_ready_no_exp_date.publish)


class MeetupModelTests(TestCase):
    """Tests for custom methods of Meetup model."""

    def setUp(self):
        """Setting up models with mommy."""
        self.custom_date = timezone.now() + timedelta(days=45)
        self.meetup_not_ready = mommy.make(Meetup, review_status=Meetup.OPEN)
        self.meetup_ready_no_exp_date = mommy.make(
            Meetup,
            review_status=Meetup.READY_TO_PUBLISH,
            expiration_date=None
        )
        self.meetup_ready_custom_exp_date = mommy.make(
            Meetup,
            review_status=Meetup.READY_TO_PUBLISH,
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
