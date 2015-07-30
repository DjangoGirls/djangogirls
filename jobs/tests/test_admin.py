from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.core import mail


from model_mommy import mommy

from core.models import User
from jobs.models import Job, Meetup


class JobAdminTest(TestCase):
    """Tests for custom methods of JobAdmin model. Most importantly
    the publish flow in admin"""

    def setUp(self):
        self.admin_user = User.objects.create_superuser('myemail@test.com', 'example')
        self.future_date = timezone.now().date() + timedelta(days=10)
        self.job_open = mommy.make(
            Job,
            review_status=Job.OPEN,
        )
        self.job_under_review = mommy.make(
            Job,
            review_status=Job.UNDER_REVIEW,
            reviewer=self.admin_user,
        )
        self.job_ready_to_publish = mommy.make(
            Job,
            review_status=Job.READY_TO_PUBLISH,
            reviewer=self.admin_user,
        )
        self.job_published = mommy.make(
            Job,
            review_status=Job.PUBLISHED,
            reviewer=self.admin_user,
            published_date=timezone.now(),
            expiration_date=self.future_date,
        )
        self.job_rejected = mommy.make(
            Job,
            review_status=Job.REJECTED,
            reviewer=self.admin_user,
        )
        self.client.login(username=self.admin_user.email, password='example')

    def test_assigning_job_reviewer_to_open_post(self):
        assign_reviewer_url = reverse(
            'admin:assign_job_reviewer',
            args=[self.job_open.id]
        )
        response = self.client.get(assign_reviewer_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.job_open.refresh_from_db()
        self.assertIn("Under review", str(response.content))
        self.assertIn("myemail@test.com", str(response.content))
        self.assertEqual(self.job_open.review_status, Job.UNDER_REVIEW)

    def test_assigning_job_reviewer_to_under_review_post(self):
        """This test secures a situation when someone enters the URL manually.
        If a post is not in the OPEN state, it is not possible to execute
        the assign method and the app returns Error 400"""
        assign_reviewer_url = reverse(
            'admin:assign_job_reviewer',
            args=[self.job_under_review.id]
        )
        response = self.client.get(assign_reviewer_url, follow=True)
        self.assertEqual(response.status_code, 400)

    def test_unassigning_job_reviewer_from_under_review_post(self):
        unassign_reviewer_url = reverse(
            'admin:unassign_job_reviewer',
            args=[self.job_under_review.id]
        )
        response = self.client.get(unassign_reviewer_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.job_under_review.refresh_from_db()
        self.assertIn("Open", str(response.content))
        self.assertIn("None", str(response.content))
        self.assertEqual(self.job_under_review.review_status, Job.OPEN)

    def test_accept_job_for_under_review_post(self):
        accept_url = reverse(
            'admin:accept_job',
            args=[self.job_under_review.id]
        )
        response = self.client.get(accept_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.job_under_review.refresh_from_db()
        self.assertIn("Ready to publish", str(response.content))
        self.assertIn("myemail@test.com", str(response.content))
        self.assertEqual(self.job_under_review.review_status, Job.READY_TO_PUBLISH)

    def test_reject_job_for_under_review_post(self):
        reject_url = reverse(
            'admin:reject_job',
            args=[self.job_under_review.id]
        )
        response = self.client.get(reject_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.job_under_review.refresh_from_db()
        self.assertIn("Rejected", str(response.content))
        self.assertIn("myemail@test.com", str(response.content))
        self.assertEqual(self.job_under_review.review_status, Job.REJECTED)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Rejected", mail.outbox[0].body)
        self.assertEqual("jobs@djangogirls.org", mail.outbox[0].from_email)

    def test_reject_job_for_ready_to_publish_post(self):
        reject_url = reverse(
            'admin:reject_job',
            args=[self.job_ready_to_publish.id]
        )
        response = self.client.get(reject_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.job_ready_to_publish.refresh_from_db()
        self.assertIn("Rejected", str(response.content))
        self.assertIn("myemail@test.com", str(response.content))
        self.assertEqual(self.job_ready_to_publish.review_status, Job.REJECTED)

    def test_reject_job_for_published_post(self):
        reject_url = reverse(
            'admin:reject_job',
            args=[self.job_published.id]
        )
        response = self.client.get(reject_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.job_published.refresh_from_db()
        self.assertIn("Rejected", str(response.content))
        self.assertIn("myemail@test.com", str(response.content))
        self.assertEqual(self.job_published.review_status, Job.REJECTED)
        self.assertEqual(self.job_published.published_date, None)

    def test_restore_job_for_rejected_post(self):
        restore_url = reverse(
            'admin:restore_job',
            args=[self.job_rejected.id]
        )
        response = self.client.get(restore_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.job_rejected.refresh_from_db()
        self.assertIn("Under review", str(response.content))
        self.assertIn("myemail@test.com", str(response.content))
        self.assertEqual(self.job_rejected.review_status, Job.UNDER_REVIEW)

    def test_publish_job_for_ready_to_publish_post(self):
        publish_url = reverse(
            'admin:publish_job',
            args=[self.job_ready_to_publish.id]
        )
        response = self.client.get(publish_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.job_ready_to_publish.refresh_from_db()
        self.assertIn("Published", str(response.content))
        self.assertNotIn("(None)", str(response.content))
        self.assertEqual(self.job_ready_to_publish.review_status, Job.PUBLISHED)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Published", mail.outbox[0].body)
        self.assertEqual("jobs@djangogirls.org", mail.outbox[0].from_email)

    def tearDown(self):
        self.job_open.delete()
        self.job_under_review.delete()
        self.job_ready_to_publish.delete()
        self.job_rejected.delete()
        self.job_published.delete()
        self.admin_user.delete()
