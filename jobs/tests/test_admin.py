from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse


from model_mommy import mommy

from core.models import User
from jobs.models import Job, Meetup


class JobAdminTest(TestCase):
    """Tests for custom methods of JobAdmin model."""

    def setUp(self):
        self.job_open = mommy.make(
            Job,
            review_status=Job.OPEN,
        )
        self.admin_user = User.objects.create_superuser('myemail@test.com', 'example')
        self.client.login(username=self.admin_user.email, password='example')

    def test_assigning_job_reviewer_to_open_post(self):
        assign_reviewer_url = reverse('admin:assign_job_reviewer', args=[self.job_open.id])
        response = self.client.get(assign_reviewer_url, follow=True)
        self.assertEqual(response.status_code, 200)
        # TODO: assert model field
        self.assertIn("Under review", str(response.content))

    def tearDown(self):
        self.job_open.delete()
        self.admin_user.delete()
