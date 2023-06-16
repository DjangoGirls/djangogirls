import re
from collections import defaultdict, namedtuple
from datetime import datetime
from decimal import Decimal
from os import path

from django.utils import timezone

CSV_FILENAME_FORMAT = "%Y-%m-Patreon.csv"


BasePatron = namedtuple(
    "BasePatron",
    [
        "first_name",
        "last_name",
        "email",
        "pledge_raw",
        "lifetime_raw",
        "status",
        "twitter",
        "street",
        "city",
        "state",
        "zip",
        "country",
        "start_raw",
        "max_amount",
        "complete_raw",
    ],
)

BaseReward = namedtuple("BaseReward", ["name", "description_raw"])


class Patron(BasePatron):
    @property
    def start(self):
        if not self.start_raw:
            return None
        return datetime.strptime(self.start_raw, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)

    @property
    def pledge(self):
        return Decimal(self.pledge_raw.replace(",", ""))

    @property
    def lifetime(self):
        return Decimal(self.lifetime_raw.replace(",", ""))

    @property
    def completed(self):
        return self.complete_raw == "1"

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def shipping(self):
        return f"{self.street}\n{self.zip} {self.state}\n{self.country}".strip()


class Reward(BaseReward):
    @property
    def value(self):
        """
        Convert the reward's name (like '5.00+ Reward') to its numerical value
        (5.00).
        """
        match = re.search("^(?P<value>.+) Reward$", self.name)
        assert match is not None
        value = match.group("value")
        if value == "No":
            return 0

        assert value.endswith("+")
        return Decimal(value[:-1])

    @property
    def description(self):
        match = re.search("^Description: (?P<description>.+)$", self.description_raw)
        assert match is not None
        return match.group("description")


def guess_month_from_filename(csv_filename, datefmt=CSV_FILENAME_FORMAT):
    csv_filename = path.basename(csv_filename)
    return datetime.strptime(csv_filename, datefmt).date()


def unflatten_csv(reader):
    """
    Return a dictionary of {reward: patrons} from the given CSV file.
    """
    unflattened = defaultdict(list)

    headers = next(reader)  # skip header row
    assert len(headers) == len(Patron._fields)

    current_reward = None

    for _row in reader:
        if len(_row) == 2:
            current_reward = Reward(*_row)
            continue

        assert current_reward is not None
        unflattened[current_reward].append(Patron(*_row))

    return unflattened
