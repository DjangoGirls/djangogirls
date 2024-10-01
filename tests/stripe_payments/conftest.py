from datetime import datetime

import pytest

from stripe_payments.models import StripeCharge


@pytest.fixture
def donation():
    return StripeCharge.objects.create(
        charge_id="ch_19rVRuBN9GADq2YjQsQCfDHQ",
        amount=10,
        payment_data={
            "id": "ch_19rVRuBN9GADq2YjQsQCfDHQ",
            "paid": True,
            "order": "",
            "amount": 10,
            "object": "charge",
            "review": "",
            "source": {},
        },
        charge_created=datetime.now(),
        fetched=datetime.now(),
    )
