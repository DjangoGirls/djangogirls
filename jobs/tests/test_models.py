from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from model_mommy import mommy

from core.models import User
from jobs.models import Job, Meetup


class JobModelTests(TestCase):
    """Tests for custom methods of Job model."""

    def setUp(self):
        """Setting up models with mommy."""
        self.future_date = timezone.now().date() + timedelta(days=45)
        self.past_date = timezone.now().date() - timedelta(days=45)
        self.job_open = mommy.make(Job, review_status=Job.OPEN)
        self.job_under_review = mommy.make(Job, review_status=Job.UNDER_REVIEW)
        self.job_ready_no_exp_date = mommy.make(
            Job,
            review_status=Job.READY_TO_PUBLISH,
            expiration_date=None
        )
        self.job_ready_future_exp_date = mommy.make(
            Job,
            review_status=Job.READY_TO_PUBLISH,
            expiration_date=self.future_date
        )
        self.job_ready_past_exp_date = mommy.make(
            Job,
            review_status=Job.READY_TO_PUBLISH,
            expiration_date=self.past_date
        )
        self.job_rejected = mommy.make(Job, review_status=Job.REJECTED)
        self.job_published = mommy.make(
            Job,
            review_status=Job.PUBLISHED,
            published_date=timezone.now()
        )
        self.sample_user = mommy.make(
            User,
            first_name="Ola",
            last_name="Smith"
        )

    def test_is_ready_to_publish_for_not_ready(self):
        """Tests if the is_ready_to_publish_method returns correct value
        for a job not ready to publish"""
        self.assertFalse(self.job_open.is_ready_to_publish())

    def test_is_ready_to_publish_for_ready(self):
        """Tests if the is_ready_to_publish_method returns correct value
        for a job ready to publish"""
        self.assertTrue(self.job_ready_no_exp_date.is_ready_to_publish())

    def test_assign_for_jobs_open(self):
        """Tests the assign method for jobs in the OPEN state"""
        self.job_open.assign(self.sample_user)
        self.assertTrue(self.job_open.review_status == Job.UNDER_REVIEW)
        self.assertTrue(self.job_open.reviewer == self.sample_user)

    def test_assign_for_jobs_not_open(self):
        """Tests the assign method for jobs not in the OPEN state"""
        self.assertRaises(AssertionError, self.job_under_review.assign, self.sample_user)

    def test_unassign_for_jobs_under_review(self):
        """Tests the unassign method for jobs in the UNDER_REVIEW state"""
        self.job_under_review.unassign()
        self.assertTrue(self.job_under_review.review_status == Job.OPEN)
        self.assertFalse(self.job_under_review.reviewer)

    def test_unassign_for_jobs_not_under_review(self):
        """Tests the unassign method for jobs not in the UNDER_REVIEW state"""
        self.assertRaises(AssertionError, self.job_open.unassign)

    def test_accept_for_jobs_under_review(self):
        """Tests the accept method for jobs in the UNDER_REVIEW state"""
        self.job_under_review.accept()
        self.assertTrue(self.job_under_review.review_status == Job.READY_TO_PUBLISH)

    def test_accept_for_jobs_not_under_review(self):
        """Tests the unassign method for jobs not in the UNDER_REVIEW state"""
        self.assertRaises(AssertionError, self.job_open.accept)

    def test_reject_for_jobs_under_review(self):
        """Tests the reject method for jobs in the UNDER_REVIEW state"""
        self.job_under_review.reject()
        self.assertTrue(self.job_under_review.review_status == Job.REJECTED)

    def test_reject_for_jobs_ready_to_publish(self):
        """Tests the reject method for jobs in the READY_TO_PUBLISHED state"""
        self.job_ready_no_exp_date.reject()
        self.assertTrue(self.job_ready_no_exp_date.review_status == Job.REJECTED)

    def test_reject_for_jobs_published(self):
        """Tests the reject method for jobs in the PUBLISHED state"""
        self.job_published.reject()
        self.assertTrue(self.job_published.review_status == Job.REJECTED)
        self.assertFalse(self.job_published.published_date)

    def test_reject_for_jobs_in_wrong_state(self):
        """Tests the reject method for jobs not in the wrong state"""
        self.assertRaises(AssertionError, self.job_open.reject)

    def test_restore_for_jobs_rejected(self):
        """Tests the restore method for jobs in the REJECTED state"""
        self.job_rejected.restore(self.sample_user)
        self.assertTrue(self.job_rejected.review_status == Job.UNDER_REVIEW)
        self.assertTrue(self.job_rejected.reviewer == self.sample_user)

    def test_restore_for_jobs_not_rejected(self):
        """Tests the restore method for jobs not in the REJECTED state"""
        self.assertRaises(AssertionError, self.job_open.restore, self.sample_user)

    def test_publish_not_ready_to_publish(self):
        """Attempts to publish jobs which are not in the READY_TO_PUBLISH state,
        it should results in an assertion error"""
        self.assertRaises(AssertionError,  self.job_open.publish)

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
        self.job_ready_future_exp_date.publish()
        self.assertEqual(
            self.job_ready_future_exp_date.expiration_date,
            self.future_date
        )

    def test_publish_expired_post(self):
        """Tests the publish method with past expiration date. It might happen
         if the expired post is rejected and than re-published"""
        self.job_ready_past_exp_date.publish()
        self.assertTrue(self.job_ready_past_exp_date.published_date)
        self.assertAlmostEqual(
            self.job_ready_past_exp_date.published_date,
            timezone.now(),
            delta=timedelta(seconds=10)
        )
        self.assertTrue(self.job_ready_past_exp_date.expiration_date)
        result = self.job_ready_past_exp_date.expiration_date - timezone.now()
        self.assertEqual(result.days, 59)

    def test_publish_twice_in_a_row(self):
        """It is not possible to publish a job opportunity twice"""
        self.assertFalse(self.job_ready_no_exp_date.published_date)
        self.job_ready_no_exp_date.publish()
        self.assertTrue(self.job_ready_no_exp_date.published_date, "Job has no published date.")
        self.assertRaises(AssertionError, self.job_ready_no_exp_date.publish)


class MeetupModelTests(TestCase):
    """Tests for custom methods of Meetup model."""

    def setUp(self):
        """Setting up models with mommy."""
        self.future_date = timezone.now().date() + timedelta(days=45)
        self.meetup_not_ready = mommy.make(Meetup, review_status=Meetup.OPEN)
        self.meetup_ready_no_exp_date = mommy.make(
            Meetup,
            review_status=Meetup.READY_TO_PUBLISH,
            expiration_date=None
        )
        self.meetup_ready_future_exp_date = mommy.make(
            Meetup,
            review_status=Meetup.READY_TO_PUBLISH,
            expiration_date=self.future_date
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
        self.meetup_ready_future_exp_date.publish()
        self.assertEqual(
            self.meetup_ready_future_exp_date.expiration_date,
            self.future_date
        )
