from django.core.mail import send_mail

from djangogirls.settings import JOBS_EMAIL_USER, JOBS_EMAIL_PASSWORD
from djangogirls.settings import MEETUPS_EMAIL_PASSWORD, MEETUPS_EMAIL_USER


def send_job_mail(subject, message_plain, message_html, recipient):
    send_from = "jobs@djangogirls.org"
    send_mail(
        subject,
        message_plain,
        send_from,
        [recipient, send_from],
        auth_user=JOBS_EMAIL_USER,
        auth_password=JOBS_EMAIL_PASSWORD,
        html_message=message_html
    )


def send_meetup_mail(subject, message_plain, message_html, recipient):
    send_from = "meetups@djangogirls.org"
    send_mail(
        subject,
        message_plain,
        send_from,
        [recipient, send_from],
        auth_user=MEETUPS_EMAIL_USER,
        auth_password=MEETUPS_EMAIL_PASSWORD,
        html_message=message_html
    )
