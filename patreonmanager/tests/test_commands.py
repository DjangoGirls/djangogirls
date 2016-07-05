import datetime

from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO

from ..models import Patron, Payment, Reward


class CommandsTestCase(TestCase):
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

    def test_listpatrons(self):
        payments = Payment.objects.filter(
            status=Payment.STATUS.PROCESSED,
            completed=False,
            reward__value__gte=10,
        )
        self.assertEqual(payments.count(), 1)
        out = StringIO()
        call_command('listpatrons', stdout=out)
        print(out.getvalue())
        self.assertIn('in a row', out.getvalue())
