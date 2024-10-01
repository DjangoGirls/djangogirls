from datetime import datetime, timezone

from django.db import models


class StripeChargeManager(models.Manager):
    def create_from_stripe_charge_data(self, stripe_charge_data):
        """Create a StripeCharge from Stripe Charge data."""
        return self.create(
            charge_id=stripe_charge_data["id"],
            amount=stripe_charge_data["amount"],
            payment_data=stripe_charge_data,
            charge_created=datetime.fromtimestamp(stripe_charge_data["created"], tz=timezone.utc),
            fetched=datetime.now(tz=timezone.utc),
        )

    def running_total(self, since=None):
        qs = self.get_queryset()
        if since is not None:
            qs = qs.filter(charge_created__gte=since)
        return qs.aggregate(total=models.Sum("amount"))


class StripeCharge(models.Model):
    """
    Holds Stripe Charge data.

    Fetched via the API. Used to populate the Invoice.
    """

    charge_id = models.CharField(max_length=255, unique=True, editable=False)
    amount = models.IntegerField()
    payment_data = models.JSONField()
    charge_created = models.DateTimeField()
    fetched = models.DateTimeField()

    objects = StripeChargeManager()

    def __str__(self):
        return self.charge_id
