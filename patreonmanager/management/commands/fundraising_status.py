import logging

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from slacker import Error as SlackerError

from core.slack_client import slack

from ...models import FundraisingStatus


DJANGOGIRLS_USER_ID = 483065
BASE_API_URL = 'https://api.patreon.com/'


class Command(BaseCommand):
    help = 'Fetch current amount of money raised on our Patreon'

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO)

        logging.info("Trying to fetch data from Patreon...")
        url = f"{BASE_API_URL}user/{DJANGOGIRLS_USER_ID}"
        request = requests.get(url)
        data = request.json()

        patron_count = data['linked'][0]['patron_count']
        pledge_sum = int(int(data['linked'][0]['pledge_sum']) / 100)
        message = (
            f"Daily Patreon update: {patron_count} patrons pledged ${pledge_sum} monthly!"
        )
        logging.info(message)

        stats = FundraisingStatus(number_of_patrons=patron_count,
                                  amount_raised=pledge_sum)
        stats.save()
        logging.info("Stats saved.")

        if settings.ENABLE_SLACK_NOTIFICATIONS:
            try:
                slack.chat.post_message(
                    channel='#notifications',
                    text=message,
                    username='Django Girls',
                    icon_emoji=':django_heart:'
                )
            except SlackerError:
                logging.warning("Slack message not sent.")
