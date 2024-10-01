# Management command to fetch Stripe charges from the API since the last fetch
# and store them in the database as StripeCharge objects.

import logging

import stripe
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from stripe_payments.models import StripeCharge

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        "Fetch Stripe charges from the API since the last fetch and store them in the "
        "database as StripeCharge objects."
    )

    def handle(self, *args, **options):
        logger.debug(
            "Fetching Stripe charges from the API since the last fetch and storing "
            "them in the database as StripeCharge objects."
        )
        # Get the last StripeCharge fetched.
        try:
            last_fetched = StripeCharge.objects.order_by("-fetched").first().fetched
        except AttributeError:
            # No StripeCharge objects exist.
            last_fetched = None
        # Fetch the Stripe charges.
        stripe.api_key = settings.STRIPE_API_KEY
        # stripe.api_version = settings.STRIPE_API_VERSION

        # Fetch the Stripe charges.
        stripe_charges = stripe.Charge.list(
            limit=100,
            created={"gt": int(last_fetched.timestamp())} if last_fetched else None,
            expand=["data.customer", "data.customer.tax_ids"],
        )
        logger.info(len(stripe_charges), "Stripe charges fetched.")
        with transaction.atomic():
            for stripe_charge in stripe_charges:
                StripeCharge.objects.create_from_stripe_charge_data(stripe_charge)
        logger.debug(
            "Fetched Stripe charges from the API since the last fetch and stored them "
            "in the database as StripeCharge objects."
        )
