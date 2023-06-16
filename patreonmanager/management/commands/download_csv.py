import logging
from getpass import getpass
from os import path

from django.core.management.base import BaseCommand

from ...utils.download import _download, gen_monthly_report_links, login


class Command(BaseCommand):
    help = "Download your monthly patron reports from Patreon (CSV)."

    def add_arguments(self, parser):
        parser.add_argument("-u", "--username", help="Patreon username")
        parser.add_argument("-p", "--password", help="Patreon password")
        parser.add_argument("-d", "--directory", help="save CSV reports to DIRECTORY", default=".")

    def handle(self, *args, **options):
        if not options["username"]:
            options["username"] = input("Patreon username: ")
        if not options["password"]:
            options["password"] = getpass("Patreon password (will be hidden): ")

        if options["verbosity"] > 0:
            logging.basicConfig(level=logging.INFO)

        session = login(options["username"], options["password"])

        for filename, url in gen_monthly_report_links(session):
            _download(session, url, path.join(options["directory"], filename))
