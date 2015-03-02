# encoding: utf-8

from django.test import TestCase
from django.core.urlresolvers import reverse

from jobs.models import Job, Company


class JobCreateTests(TestCase):
    def setUp(self):
        Company.objects.create(
            name="My Company",
            website="http://mycompany.com/"
        )
        self.context = {
            'company_name': 'My Company',
            'website': 'http://mycompany.com',
            'contact_email': 'jobs@company.com',
            'title': 'Job offer',
            'description': 'description',
            'city': u'Kraków',
            'country': 'PL',
            'save': True,
        }

    def test_job_add_new_company_clean(self):
        """Tests adding a new job with a new company"""
        context = self.context
        context['company_name'] = 'New Company'
        context['website'] = 'http://newcompany.com'
        response = self.client.post(reverse('jobs:job_new'), context)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Job.objects.get(company__name="New Company", title="Job offer")
        )

    def test_job_add_existing_company_clean(self):
        """Tests adding a new job with an existing company"""
        context = self.context
        response = self.client.post(reverse('jobs:job_new'), context)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Job.objects.get(company__name="My Company", title="Job offer")
        )

    def test_job_add_existing_company_with_different_website(self):
        """Tests adding a new job by a company which already exists but with
         a different website. User should get a validation error and
         two buttons to make the decision: overwrite or keep"""
        context = self.context
        context['website'] = 'http://company.com'
        response = self.client.post(reverse('jobs:job_new'), context)
        self.assertEqual(response.status_code, 200)
        self.assertIn("already exists", response.content)
        self.assertIn("overwrite", response.content)
        self.assertIn("keep", response.content)

    def test_job_add_existing_company_with_different_website_overwrite(self):
        """Tests adding a new job by a company which already exists but with
        a different website when user chooses to overwrite the old website"""
        context = self.context
        context['website'] = 'http://company.com'
        del context['save']
        context['overwrite'] = True
        response = self.client.post(reverse('jobs:job_new'), context)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Job.objects.get(company__name="My Company", title="Job offer")
        )
        self.assertEqual(Company.objects.get(name="My Company").website,
                         'http://company.com/')

    def test_job_add_existing_company_with_different_website_keep(self):
        """Tests adding a new job by a company which already exists but with
        a different website when user chooses to keep the old website"""
        context = self.context
        context['website'] = 'http://company.com'
        del context['save']
        context['keep'] = True
        response = self.client.post(reverse('jobs:job_new'), context)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Job.objects.get(company__name="My Company", title="Job offer")
        )
        self.assertEqual(Company.objects.get(name="My Company").website,
                         'http://mycompany.com/')
