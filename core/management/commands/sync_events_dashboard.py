import datetime
import re
import time
from collections import namedtuple

from django.conf import settings
from django.core.management.base import BaseCommand
from trello import ResourceUnavailable, TrelloClient

from core.models import Event

# Create new command


class Command(BaseCommand):
    help = "Syncs event in trello board. Need a token."
    missing_args_message = (
        "You need to add a token! Get one here: "
        "https://trello.com/1/authorize?key=01ab0348ca020573e7f728ae7400928a&scope=read%2Cwrite&"
        "name=My+Application&expiration=1hour&response_type=token"
    )

    def add_arguments(self, parser):
        parser.add_argument("trello_token", type=str)

    def handle(self, *args, **options):
        token = options["trello_token"]
        events = event_list()
        sync(events, token)


# Get data


EventTuple = namedtuple("EventTuple", "name id city date")


def event_list():
    event = Event.objects.all()
    result = []
    for e in event:
        name = e.name
        _id = str(e.pk)
        city = e.city
        date = datetime.date(e.date.year, e.date.month, e.date.day or 1)
        result.append(EventTuple(name, _id, city, date))
    return result


# Sync to trello


ADMIN_BASE_URL = "https://djangogirls.org/admin/core/event/"


def sync(events, token):
    trello = TrelloClient(api_key=settings.TRELLO_API_KEY, token=token)
    board = trello.get_board("55f7167c46760fcb5d68b385")

    far_away, less_2_months, less_1_month, less_1_week, today, past = board.all_lists()

    all_cards = {card_id(c): c for c in board.all_cards()}

    date_today = datetime.date.today()

    for e in events:
        card = all_cards.get(e.id)

        if not card:
            card = create_card(e, far_away)
            create_checklist(card)

        # fetch card to get due date
        try:
            card.fetch()
        except ResourceUnavailable:
            print("Oopsie: too many requests! Let's wait 10 seconds!")
            time.sleep(10)
            card.fetch()

        if e.date != card.due_date.date():
            print(f"Changing due date of {e.city} to {e.date}")
            card.set_due(e.date)

        distance = (e.date - date_today).days
        if distance < 0:
            right_list = past
        elif distance == 0:
            right_list = today
        elif distance < 7:
            right_list = less_1_week
        elif distance < 30:
            right_list = less_1_month
        elif distance < 60:
            right_list = less_2_months
        else:
            right_list = far_away

        ensure_card_in_list(card, right_list)


def card_id(card):
    m = re.search(ADMIN_BASE_URL + r"(\d+)", card.desc)
    return m.group(1)


def create_card(event, list):
    print(f"Creating card {event.city} ({event.date.isoformat()})")
    return list.add_card(name=event.city, desc=ADMIN_BASE_URL + event.id, due=event.date.isoformat())


def create_checklist(card):
    card.add_checklist(
        "Things to do:", ["2 month check", "1 month check", "Thank you email and request for stats", "Stats obtained"]
    )


def ensure_checklist_in_card(card):
    if not card.checklists:
        print(f"Adding checklist to {card.name} card.")
        create_checklist(card)


def ensure_card_in_list(card, list):
    if card.list_id != list.id:
        print(f"Moving {card.name} to {list.name}")
        card.change_list(list.id)
