import datetime

from patreonmanager.admin import PatronAdmin
from patreonmanager.filters import PendingRewardsFilter
from patreonmanager.models import Patron, Payment


def test_pending_rewards(patron, reward, payment):
    filter = PendingRewardsFilter(None, {"pending_rewards": "true"}, Patron, PatronAdmin)
    patrons = filter.queryset(None, Patron.objects.all())
    assert len(patrons) == 0

    Payment.objects.create(
        status=Payment.STATUS.PROCESSED,
        completed=False,
        reward=reward,
        patron=patron,
        pledge="20.00",
        month=datetime.date(2016, 2, 20),
    )

    Payment.objects.create(
        status=Payment.STATUS.PROCESSED,
        completed=False,
        reward=reward,
        patron=patron,
        pledge="20.00",
        month=datetime.date(2016, 3, 20),
    )

    patrons = filter.queryset(None, Patron.objects.all())
    assert len(patrons) == 1
    assert patrons[0].pk == patron.pk
