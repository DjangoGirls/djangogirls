import csv
import logging

from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware

from ...models import Patron, Payment, Reward
from ...utils.csv import guess_month_from_filename, unflatten_csv


class Command(BaseCommand):
    help = "Import the Patreon CSV reports into the database."

    def add_arguments(self, parser):
        parser.add_argument("csv_filenames", nargs="+")
        parser.add_argument("--create-rewards", help="create missing rewards if needed", action="store_true")

    def handle(self, *args, **options):
        if options["verbosity"] > 0:
            logging.basicConfig(level=logging.INFO)

        data = {}

        for csv_filename in sorted(options["csv_filenames"]):
            month = guess_month_from_filename(csv_filename)
            with open(csv_filename) as f:
                reader = csv.reader(f)
                data[month] = unflatten_csv(reader)

        for month, month_data in sorted(data.items(), key=lambda t: t[0]):
            for reward_t, patrons in month_data.items():
                if options["create_rewards"]:
                    defaults = {"description": reward_t.description, "value": reward_t.value}
                    reward, created = Reward.objects.get_or_create(name=reward_t.name, defaults=defaults)
                    if created:
                        logging.info("Created reward object with name %r.", reward.name)
                else:
                    reward = Reward.objects.get(name=reward_t.name)

                for patron_t in patrons:
                    defaults = {
                        "name": patron_t.name,
                        "twitter": patron_t.twitter,
                        "address": patron_t.shipping,
                        "since": make_aware(patron_t.start),
                    }
                    patron, created = Patron.objects.update_or_create(email=patron_t.email, defaults=defaults)
                    if created:
                        logging.info("Created patron object with email %r.", patron.email)
                    else:
                        logging.info("Updated patron object with email %r.", patron.email)

                    defaults = {
                        "reward": reward,
                        "pledge": patron_t.pledge,
                        "status": getattr(Payment.STATUS, patron_t.status.upper()),
                        "completed": patron_t.completed,
                    }
                    payment, created = Payment.objects.get_or_create(patron=patron, month=month, defaults=defaults)
                    if created:
                        msg = "Created Payment for month %s and patron %s."
                        logging.info(msg, payment.get_month_display(), patron)
