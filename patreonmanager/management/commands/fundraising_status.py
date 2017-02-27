import logging

import requests
from django.core.management.base import BaseCommand
from slacker import Error as SlackerError

from core.slack_client import slack

from ...models import FundraisingStatus
from core.utils import opbeat_logging

DJANGOGIRLS_USER_ID = 483065
BASE_API_URL = 'http://api.patreon.com/'


class Command(BaseCommand):
    help = 'Fetch current amount of money raised on our Patreon'

    @opbeat_logging()
    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO)

        logging.info("Trying to fetch data from Patreon...")
        url = "{}user/{}".format(BASE_API_URL, DJANGOGIRLS_USER_ID)
        request = requests.get(url)
        data = request.json()

        patron_count = data['linked'][0]['patron_count']
        pledge_sum = int(int(data['linked'][0]['pledge_sum'])/100)
        message = (
            "Daily Patreon update: {} patrons pledged ${} monthly!".format(
                patron_count, pledge_sum))
        logging.info(message)

        stats = FundraisingStatus(number_of_patrons=patron_count,
                                  amount_raised=pledge_sum)
        stats.save()
        logging.info("Stats saved.")

        try:
            slack.chat.post_message(
                channel='#notifications',
                text=message,
                username='Django Girls',
                icon_emoji=':django_heart:'
            )
        except SlackerError:
            logging.warning("Slack message not sent.")
