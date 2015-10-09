from collections import Counter

from django.core.management.base import BaseCommand

from ...models import Payment


class Command(BaseCommand):
    help = 'List Patrons who need a reward to be sent to them'

    def handle(self, *args, **options):
        payments = Payment.objects.filter(
            status=Payment.STATUS.PROCESSED,
            completed=False,
            reward__value__gte=10,
        )

        c = Counter(payment.patron for payment in payments.select_related('patron'))

        for patron, count in c.most_common():
            if count < 3:
                break
            self.stdout.write("%s: %d months" % (patron.name, count))
