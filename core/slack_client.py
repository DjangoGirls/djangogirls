from django.conf import settings
from slacker import Slacker

slack = Slacker(settings.SLACK_API_KEY)


def user_invite(email, first_name):
    return slack.users.post('users.admin.invite', params={
        'email': email,
        'first_name': first_name,
        'set_active': True
    })
