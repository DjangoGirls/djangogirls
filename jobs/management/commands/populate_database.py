import random

import os

from django.core.management.base import NoArgsCommand

from jobs.models import Company, Job, Meetup


def read_lines():
    """Reads random lines from a file to generate description."""
    name = 'jobs/management/commands/description.txt'
    if os.path.isfile(name):
        with open(name, 'r') as f:
            all_lines = f.read().splitlines()
            for i in range(0, 4):
                selected_lines = random.choice(all_lines)
                description = ''.join(selected_lines)
    else:
        description = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
    return description


class Command(NoArgsCommand):
    help = "Populates database with meetups, companies and job offers."

    def add_meetup(self, title, city, country, description, meetup_date):
        meetup = Meetup.objects.get_or_create(
            title=title,
            contact_email='example@example.com',
            city=city,
            country=country,
            description=description,
            ready_to_publish=True,
            meetup_date=meetup_date,
        )
        return meetup

    def add_company(self, name, website):
        company = Company.objects.get_or_create(
            name=name,
            website=website
        )
        return company

    def add_job(self, title, company, city, country, description):
        job = Job.objects.get_or_create(
            title=title,
            company=company,
            contact_email='example@example.com',
            city=city,
            country=country,
            description=description,
            ready_to_publish=True,
        )
        return job

    def handle_noargs(self, **options):
        # Adding some meetups with future dates.
        self.add_meetup(
            title='Django Girls Warsaw',
            city='Warsaw',
            country='PL',
            description=read_lines(),
            meetup_date='2015-04-01'
        )
        self.add_meetup(
            title='Women in Technology',
            city='London',
            country='GB',
            description=read_lines(),
            meetup_date='2015-05-15'
        )
        self.add_meetup(
            title='Learn javascript',
            city='Paris',
            country='FR',
            description=read_lines(),
            meetup_date='2015-06-12'
        )

        self.add_meetup(
            title='Python breakfast',
            city='Berlin',
            country='DE',
            description=read_lines(),
            meetup_date='2015-07-01'
        )

        self.add_meetup(
            title='Girls Meetup',
            city='New York',
            country='US',
            description=read_lines(),
            meetup_date='2015-08-01'
        )

        # Adding some companies.
        self.add_company(
            name='Google',
            website='http://www.google.pl/about/careers/students/'
        )

        self.add_company(
            name='Amazon',
            website='http://www.amazon.jobs/team-category/university-recruiting'
        )

        self.add_company(
            name='Digital Ocean',
            website='https://careers.digitalocean.com/'
        )

        # Adding some job offers.
        self.add_job(
            title='Intern',
            company=Company.objects.get(name='Google'),
            city='London',
            country='GB',
            description=read_lines(),
        )

        self.add_job(
            title='Software Development Engineer - Paid Internship',
            company=Company.objects.get(name='Amazon'),
            city='Gdansk',
            country='PL',
            description=read_lines(),
        )

        self.add_job(
            title='Software Engineer, Front End',
            company=Company.objects.get(name='Digital Ocean'),
            city='New York',
            country='US',
            description=read_lines(),
        )

        def print_created_objects(model):
            """Prints created objects on terminal."""
            for created_object in model.objects.all():
                self.stdout.write('-{0}'.format(created_object))

        # Publishing meetups and job offers.
        for meetup in Meetup.objects.all():
            meetup.publish()
        for job in Job.objects.all():
            job.publish()

        print_created_objects(Meetup)
        print_created_objects(Company)
        print_created_objects(Job)
