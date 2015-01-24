from django.test import TestCase
from django.utils import timezone

from model_mommy import mommy

from jobs.models import Job


class JobModelTests(TestCase):
    """Tests for custom methods of Job model."""

    """Setting up models with mommy."""
    def setUp(self):
        self.job = mommy.make(Job, ready_to_publish=True)
        self.job1 = mommy.make(Job, ready_to_publish=False)

    """Plain publish method test without any twists."""
    def test_publish_succesfully(self):
        self.assertFalse(self.job.published_date)
        self.job.publish()
        self.assertTrue(self.job.published_date, "Job has no published date.")

    """Publish doesn't work when ready_to_publish field is set to False."""
    def test_publish_unsuccesfully(self):
        self.assertFalse(self.job1.published_date)
        self.job1.publish()
        self.assertFalse(self.job1.published_date, "Job has published date.")

    """Publish once, than change ready_to_publish field value and publish once more."""
    def test_publish_more_than_once_and_change_values(self):
        self.assertFalse(self.job.published_date)
        self.job.publish()
        self.job.ready_to_publish == False
        # Right now if we change ready_to_publish to False, published_date stays as it was and doesn't become None.
        self.assertTrue(self.job.published_date)
        self.job.ready_to_publish == True
        self.job.publish()
        self.assertTrue(self.job.published_date, "Job has no published date.")

    """Publish twice in a row."""
    def test_publish_twice_in_a_row(self):
        self.assertFalse(self.job.published_date)
        self.job.publish()
        self.job.publish()
        self.assertTrue(self.job.published_date, "Job has no published date.")

    """Publish without review."""
    def test_publish_without_review(self):
        assertFalse(self.job.review_status, "Job was already reviewed.")
        self.job.publish()
        self.assertTrue(self.job.published_date, "Job has no published date.")


    """Test if default value is set."""
    def test_set_expiration_date(self):
        self.job.publish()
        self.assertFalse(self.job.expiration_date)
        self.job.set_expiration_date()
        self.assertTrue(self.job.expiration_date, "Job has no expiration date.")

    """Test if default value is 60 days from now."""
    def test_expiration_date_default_value(self):
        self.job.publish()
        self.assertFalse(self.job.expiration_date)
        self.job.set_expiration_date()
        result = self.job.expiration_date - timezone.now()
        self.assertEqual(result.days, 59)

    """Test setting expiration date if job is unpublished."""
    def test_expiration_date_on_not_ready(self):
        value = self.job.set_expiration_date()
        self.assertEqual(value, "Error")
        self.assertFalse(self.job.expiration_date)

    """Test setting expiration date more than once in a row."""
    def test_set_expiration_date_twice(self):
        self.job.publish()
        self.assertFalse(self.job.expiration_date)
        self.job.set_expiration_date()
        self.assertTrue(self.job.expiration_date, "Job has no expiration date.")
        self.job.set_expiration_date()
        self.assertTrue(self.job.expiration_date, "Job has no expiration date.")
