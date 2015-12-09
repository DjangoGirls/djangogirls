import logging
import requests

from django.conf import settings
from django.core.management.base import BaseCommand
from slacker import Slacker

from ...models import FundraisingStatus


# https://github.com/oxguy3/patreon-api
API_KEY = '1745177328c8a1d48100a9b14a1d38c1'
DJANGOGIRLS_USER_ID = 483065
BASE_API_URL = 'http://api.patreon.com/'

slack = Slacker(settings.SLACK_API_KEY)


class Command(BaseCommand):
    help = 'Fetch current amount of money raised on our Patreon'

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO)

        logging.info("Trying to fetch data from Patreon...")
        url = "{}user/{}".format(BASE_API_URL, DJANGOGIRLS_USER_ID)
        request = requests.get(url)
        data = request.json()

        patron_count = data['linked'][0]['patron_count']
        pledge_sum = int(int(data['linked'][0]['pledge_sum'])/100)
        message = "Daily Patreon update: {} patrons pledged ${} monthly!".format(patron_count, pledge_sum)
        logging.info(message)

        stats = FundraisingStatus(number_of_patrons=patron_count, amount_raised=pledge_sum)
        stats.save()
        logging.info("Stats saved.")

        slack.chat.post_message(
            channel='#notifications',
            text=message,
            username='Django Girls',
            icon_emoji=':django_heart:'
        )
