from patreonmanager.models import FundraisingStatus, Payment


def test_payment_str(payment):
    payment = Payment.objects.get()
    assert str(payment) == f"{payment.patron}, {payment.month}"


def test_fundraisingstatus_str():
    status = FundraisingStatus.objects.create(number_of_patrons=1, amount_raised=1)
    assert str(status) == f"{status.id} updated {status.date_updated}, raised {status.amount_raised}"
