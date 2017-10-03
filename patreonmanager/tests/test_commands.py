import datetime

from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO
from django.utils.timezone import make_aware

import vcr
import pytest

from ..models import Patron, Payment, Reward


@pytest.fixture
def patron(db):
    patron = Patron.objects.create(
        name="Jan Kowalski",
        email="jan@kowalski.extra",
        since=make_aware(datetime.datetime(2016, 1, 20)))
    reward = Reward.objects.create(
        name="gte_10",
        value=11)
    payment = Payment.objects.create(
        status=Payment.STATUS.PROCESSED,
        completed=False,
        reward=reward,
        patron=patron,
        pledge="20.00",
        month=datetime.date(2016, 1, 20))
    return patron


def test_listpatrons(patron):
    payments = Payment.objects.filter(
        status=Payment.STATUS.PROCESSED,
        completed=False,
        reward__value__gte=10,
    )
    assert payments.count() == 1
    out = StringIO()
    call_command('listpatrons', stdout=out)
    assert 'in a row' in out.getvalue()


@vcr.use_cassette('patreonmanager/tests/vcr/patreon.yaml')
def test_fundraising_status(patron):
    call_command('fundraising_status')
