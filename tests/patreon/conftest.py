import datetime

import pytest
from django.utils.timezone import make_aware

from patreonmanager.models import Patron, Payment, Reward


@pytest.fixture
def patron(db):
    return Patron.objects.create(
        name="Jan Kowalski", email="jan@kowalski.extra", since=make_aware(datetime.datetime(2016, 1, 20))
    )


@pytest.fixture
def reward(db):
    return Reward.objects.create(name="gte_10", value=11)


@pytest.fixture
def payment(db, patron, reward):
    return Payment.objects.create(
        status=Payment.STATUS.PROCESSED,
        completed=False,
        reward=reward,
        patron=patron,
        pledge="20.00",
        month=datetime.date(2016, 1, 20),
    )
