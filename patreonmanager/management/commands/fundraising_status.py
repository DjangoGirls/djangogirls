import logging

import requests
from django.core.management.base import BaseCommand
from slacker import Error as SlackerError

from slack_client.utils import get_connection as get_slack_connection

from ...models import FundraisingStatus

DJANGOGIRLS_USER_ID = 483065
BASE_API_URL = 'http://api.patreon.com/'


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
        message = (
            "Daily Patreon update: {} patrons pledged ${} monthly!".format(
                patron_count, pledge_sum))
        logging.info(message)

        stats = FundraisingStatus(number_of_patrons=patron_count,
                                  amount_raised=pledge_sum)
        stats.save()
        logging.info("Stats saved.")

        try:
            conn = get_slack_connection()
            conn.chat.post_message(
                channel='#notifications',
                text=message,
                username='Django Girls',
                icon_emoji=':django_heart:'
            )
        except SlackerError:
            logging.warning("Slack message not sent.")
