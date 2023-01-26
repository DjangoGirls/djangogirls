from io import StringIO

import vcr
from django.core.management import call_command

from patreonmanager.models import Payment


def test_listpatrons(payment):
    payments = Payment.objects.filter(
        status=Payment.STATUS.PROCESSED,
        completed=False,
        reward__value__gte=10,
    )
    assert payments.count() == 1
    out = StringIO()
    call_command("listpatrons", stdout=out)
    assert "in a row" in out.getvalue()


@vcr.use_cassette("tests/patreon/vcr/patreon.yaml")
def test_fundraising_status(patron):
    call_command("fundraising_status")
