#!/usr/bin/env python
import os
import sys

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(filename=".environment"))


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangogirls.settings")

    from django.core.management import execute_from_command_line

    if os.environ.get("CLEAN_PYC") == "TRUE" and "clean_pyc" not in sys.argv:
        # sys.stdout.write('\nCleaning .pyc files...')
        proj, _ = os.path.split(__file__)
        cmd = "find '{d}' -name '*.pyc' -delete".format(d=proj or ".")
        os.system(cmd)
        # sys.stdout.write('done\n\n')

    execute_from_command_line(sys.argv)
