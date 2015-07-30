[![Build Status](https://travis-ci.org/djangogirlsjobs/djangogirls.svg?branch=travis)](https://travis-ci.org/djangogirlsjobs/djangogirls)
[![Coverage Status](https://coveralls.io/repos/djangogirlsjobs/djangogirls/badge.svg)](https://coveralls.io/r/djangogirlsjobs/djangogirls)
(Coverage for jobs app only)

# Django Girls Community sub-page

This app adds the Community sub-page to the [Django Girls](http://djangogirls.org/) main website.
It can be a place where many post-workshop Django Girls community things may happen.

At the moment, it's not linked from the main page menu, but you can access it by adding `/community`
to the main URL or using the `Job opportunities` and `Meetups` links in the footer.

## What's in it?

For now, there are 4 tabs there:
- __Community__ - the main page of this sub-page
- __Jobs__ - a place for listing and adding job opportunities
- __Meetups__ - a place for listing and adding meetup ads
- __Blog__ - a link to Django Girls blog; it's just an example of how the sub-page can be extended with other bits

## How to add a job opportunity or a meetup ad?

On the __Jobs__ and __Meetup__ tabs respectively, there is a button to add a new post.
All jobs opportunities and meetups are moderated, so if you submit one, you'll need to wait until it's reviewed.
You'll receive an email notification once your post is accepted or rejected.

By default, each post is displayed for _60 days_ since it is published but if you prefer otherwise,
please set an expiration date on the form.

## How does the review process work?

The posts are reviewed in the django admin site. Job opportunities and meetups are visible for:
- admin users
- staff users with the `reviewers` group

Reviewers can only edit posts or publish them. They cannot add or delete posts. This can be changed if needed.

### Publish flow

A post needs to go through the following stages:

    Open -> Under review -> Ready to publish -> Published

Once a new job opportunity or a meetup is submitted, an automatic notification is sent to a person who post it
and to jobs@djangogirls.org or meetups@djangogirls.org inbox.

__Tip:__ Flow buttons are displayed in the __Tools__ section in the post details view on the right,
 underneath the __Save__ button group.

On each stage, it is possible to reject a post. Rejected posts can be restored and reviewed again if needed.

### Email notifications

Automatic notifications are sent to the contact email address when:
- a new post is submitted
- a post is accepted
- a post is rejected

If you need to convey any additional info, please fill in the __Message to organisation__ field in the __Flow info__ section.
It will be added to the email template.

On each stage, it is also possible to send a status update manually from the jobs/meetup list view using admin actions.


## Setting up an app
  
Update the required dependencies:

    pip install -r requirements.txt

Run migrations:

    ./manage.py migrate jobs
  
Create the following environment variables as listed in the `settings.py` file:

    JOBS_EMAIL_USER = os.environ.get('JOBS_EMAIL_USER')
    JOBS_EMAIL_PASSWORD = os.environ.get('JOBS_EMAIL_PASSWORD')

    MEETUPS_EMAIL_USER = os.environ.get('MEETUPS_EMAIL_USER')
    MEETUPS_EMAIL_PASSWORD = os.environ.get('MEETUPS_EMAIL_PASSWORD')
  
:tada: Enjoy the power of community! You're not alone.
