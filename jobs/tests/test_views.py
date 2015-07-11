# encoding: utf-8
from datetime import timedelta

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import timezone

from model_mommy import mommy

from jobs.models import Job, Meetup


class JobCreateTests(TestCase):

    def setUp(self):
        self.context = {
            'company': 'My Company',
            'website': 'http://mycompany.com',
            'contact_email': 'jobs@company.com',
            'title': 'Job offer',
            'description': 'description',
            'cities': u'Kraków',
            'country': 'PL',
            'save': True,
        }

    def test_job_add_new_company_clean(self):
        """Tests adding a new job with a new company"""
        context = self.context
        context['company'] = 'New Company'
        context['website'] = 'http://newcompany.com'
        response = self.client.post(reverse('jobs:job_new'), context)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Job.objects.get(company="New Company", title="Job offer")
        )


class MainPageTests(TestCase):

    def test_main_page_with_empty_database(self):
        response = self.client.get(reverse('jobs:main'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("No job offers yet", str(response.content))
        self.assertIn("No meetups yet", str(response.content))


class JobsPageTests(TestCase):

    def test_jobs_page_with_empty_database(self):
        response = self.client.get(reverse('jobs:jobs'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "There are no job offers at this moment.", str(response.content)
        )

    def test_jobs_page_with_job_not_ready_to_publish(self):
        mommy.make(
            Job,
            title='Intern',
            review_status=Meetup.OPEN)
        response = self.client.get(reverse('jobs:jobs'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "There are no job offers at this moment.", str(response.content)
        )

    def test_jobs_page_with_job_ready_to_publish(self):
        mommy.make(
            Job,
            title='Intern',
            review_status=Meetup.PUBLISHED,
            created=timezone.now() - timedelta(days=1),
            published_date=timezone.now(),
            expiration_date=timezone.now() + timedelta(days=45),
        )
        response = self.client.get(reverse('jobs:jobs'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Intern", str(response.content))


class MeetupsPageTests(TestCase):

    def test_meetups_page_with_empty_database(self):
        response = self.client.get(reverse('jobs:meetups'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Upcoming meetups", str(response.content))

    def test_meetups_page_with_meetup_not_ready_to_publish(self):
        mommy.make(
            Meetup,
            title='Django Girls Warsaw',
            review_status=Meetup.OPEN,
        )
        response = self.client.get(reverse('jobs:meetups'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Upcoming meetups", str(response.content))
        self.assertNotIn("Django Girls Warsaw", str(response.content))

    def test_jobs_page_with_job_ready_to_publish(self):
        mommy.make(
            Meetup,
            title='Django Girls Warsaw',
            review_status=Meetup.PUBLISHED,
            created=timezone.now() - timedelta(days=1),
            published_date=timezone.now(),
            expiration_date=timezone.now() + timedelta(days=45),
        )
        response = self.client.get(reverse('jobs:meetups'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Django Girls Warsaw", str(response.content))
