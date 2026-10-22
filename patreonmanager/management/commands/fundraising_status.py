import logging

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from slack_sdk.errors import SlackApiError

from core.slack_client import post_message_to_slack
from patreonmanager.models import FundraisingStatus

DJANGOGIRLS_USER_ID = 483065
BASE_API_URL = "https://api.patreon.com/"


class Command(BaseCommand):
    help = "Fetch current amount of money raised on our Patreon"

    def get_pledge_information(self, patreon_data) -> tuple[int, int]:
        """Sums up the patron counts and their pledge sums from
        all non-free membership tiers."""
        membership_tiers = patreon_data["included"]

        patron_count = 0
        pledge_sum = 0

        for tier in membership_tiers:
            attributes = tier.get("attributes", {})

            if attributes.get("is_free_tier", False):
                continue

            # Posts available for everyone are included as an "Everyone"
            # tier that doesn't have any patron count or sum information
            # so we need to use .get instead of bracket access here.
            #
            # It is not marked as a "free tier" either in the data so
            # the previous check doesn't catch it.
            patron_count += attributes.get("patron_count", 0)
            pledge_sum += int(int(attributes.get("pledge_sum", 0)) / 100)

        return patron_count, pledge_sum

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO)

        logging.info("Trying to fetch data from Patreon...")
        url = f"{BASE_API_URL}user/{DJANGOGIRLS_USER_ID}"
        request = requests.get(url)
        data = request.json()

        patron_count, pledge_sum = self.get_pledge_information(data)
        message = f"Daily Patreon update: {patron_count} patrons pledged ${pledge_sum} monthly!"
        logging.info(message)

        stats = FundraisingStatus(number_of_patrons=patron_count, amount_raised=pledge_sum)
        stats.save()
        logging.info("Stats saved.")

        if settings.ENABLE_SLACK_NOTIFICATIONS:
            try:
                post_message_to_slack("#notifications", message)
            except SlackApiError:
                logging.exception("[Daily Patreon Update] Slack message not sent.")
