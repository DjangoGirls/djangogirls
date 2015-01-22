from django.test import TestCase

from model_mommy import mommy

from jobs.models import Job


class JobMethodTests(TestCase):

	def setUp(self):
		self.job = mommy.make(Job, ready_to_publish=True)

	def test_is_published(self):
		published_date_is_not_none = False
		self.job.publish()
		if self.job.published_date:
			published_date_is_not_none = True
		self.assertEqual(published_date_is_not_none, True)
		print "Published date:{0}".format(self.job.published_date)

	def test_expiration_date(self):
		expiration_date_is_not_none = False
		self.job.publish()
		self.job.set_expiration_date()
		if self.job.expiration_date:
			expiration_date_is_not_none = True
		self.assertEqual(expiration_date_is_not_none, True)
		print "Expiration date:{0}".format(self.job.expiration_date)
