from collections import Counter

from django.contrib import admin

from .models import Payment


class PendingRewardsFilter(admin.SimpleListFilter):
    title = "Pending rewards"
    parameter_name = "pending_rewards"

    def lookups(self, request, model_admin):
        return (("true", "Show pending rewards for this month"),)

    def queryset(self, request, queryset):
        if self.value() == "true":
            patron_pks = []

            # Fetch all regular payments that hasn't been rewarded yet
            payments = Payment.objects.filter(
                status=Payment.STATUS.PROCESSED,
                completed=False,
                reward__value__gte=10,
            )
            c = Counter(payment.patron for payment in payments.select_related("patron"))
            for patron, count in c.most_common():
                # Gather pk-s of patrons who have at least 3 payments
                if count >= 3:
                    patron_pks.append(patron.pk)

            # Fetch all special payments for patrons who supported us
            # in non-financial way
            payments = Payment.objects.filter(
                status=Payment.STATUS.PROCESSED,
                completed=False,
                reward__name="Special Support Reward",
            )
            c = Counter(payment.patron for payment in payments.select_related("patron"))
            for patron, count in c.most_common():
                patron_pks.append(patron.pk)

            return queryset.filter(pk__in=set(patron_pks))

        return queryset
