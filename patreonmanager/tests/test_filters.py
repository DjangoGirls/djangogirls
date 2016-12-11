import datetime

from django.test import TestCase

from ..admin import PatronAdmin
from ..filters import PendingRewardsFilter
from ..models import Patron, Payment, Reward


class FiltersTestCase(TestCase):
    def setUp(self):
        self.patron_1 = Patron.objects.create(
            name="Jan Kowalski",
            email="jan@kowalski.extra",
            since=datetime.datetime(2016, 1, 20)
        )
        self.reward_1 = Reward.objects.create(
            name="gte_10",
            value=11
        )
        self.payment_1 = Payment.objects.create(
            status=Payment.STATUS.PROCESSED,
            completed=False,
            reward=self.reward_1,
            patron=self.patron_1,
            pledge="20.00",
            month=datetime.date(2016, 1, 20),
        )

    def test_pending_rewards(self):
        filter = PendingRewardsFilter(None, {'pending_rewards': 'true'},
                                      Patron, PatronAdmin)
        patrons = filter.queryset(None, Patron.objects.all())
        assert len(patrons) == 0

        Payment.objects.create(
            status=Payment.STATUS.PROCESSED,
            completed=False,
            reward=self.reward_1,
            patron=self.patron_1,
            pledge="20.00",
            month=datetime.date(2016, 2, 20),
        )

        Payment.objects.create(
            status=Payment.STATUS.PROCESSED,
            completed=False,
            reward=self.reward_1,
            patron=self.patron_1,
            pledge="20.00",
            month=datetime.date(2016, 3, 20),
        )

        patrons = filter.queryset(None, Patron.objects.all())
        assert len(patrons) == 1
        assert patrons[0].pk == self.patron_1.pk
