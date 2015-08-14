from smtplib import SMTPException
from django.core.mail import send_mail

from django.conf import settings


def send_job_mail(subject, message_plain, message_html, recipient):
    send_from = "jobs@djangogirls.org"
    try:
        send_mail(
            subject,
            message_plain,
            send_from,
            [recipient, send_from],
            auth_user=settings.JOBS_EMAIL_USER,
            auth_password=settings.JOBS_EMAIL_PASSWORD,
            html_message=message_html,
        )
        send_status = 'Email to {0} has been sent.'.format(''.join(recipient))
    except SMTPException:
        send_status = 'Something went wrong: email to {0}  \
            has NOT been sent.'.format(
                ''.join(recipient)
            )
    return send_status


def send_meetup_mail(subject, message_plain, message_html, recipient):
    send_from = "meetups@djangogirls.org"
    try:
        send_mail(
            subject,
            message_plain,
            send_from,
            [recipient, send_from],
            auth_user=settings.MEETUPS_EMAIL_USER,
            auth_password=settings.MEETUPS_EMAIL_PASSWORD,
            html_message=message_html,
        )
        send_status = 'Email to {0} has been sent.'.format(
            ''.join(recipient)
        )
    except SMTPException:
        send_status = 'Something went wrong: email to {0} \
            has NOT been sent.'.format(
                ''.join(recipient)
            )
    return send_status
