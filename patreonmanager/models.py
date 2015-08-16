from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Patron(models.Model):
    name = models.CharField(_("name"), max_length=200)
    email = models.EmailField(_("email"), unique=True)
    twitter = models.CharField(_("twitter"), max_length=50, blank=True)
    address = models.TextField(_("address"), blank=True)
    since = models.DateTimeField(_("patron since"), blank=True, null=True)
    last_update = models.DateTimeField(_("last update"), default=timezone.now, editable=False)

    class Meta:
        verbose_name = _("patron")
        verbose_name_plural = _("patrons")

    def __str__(self):
        return self.name


class Reward(models.Model):
    name = models.CharField(_("name"), max_length=200)
    description = models.TextField(_("description"))
    value = models.DecimalField(_("value"), max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = _("reward")
        verbose_name_plural = _("rewards")
        ordering = ['value']

    def __str__(self):
        return self.name


class STATUS(object):
    DECLINED = 'DECLINED'
    PROCESSED = 'PROCESSED'

    choices = [
        (DECLINED, _("declined")),
        (PROCESSED, _("processed")),
    ]


class PaymentQuerySet(models.QuerySet):
    def complete(self):
        return self.update(completed=True)
    complete.alters_data = True


class Payment(models.Model):
    STATUS = STATUS  # Just so that the class is available in the model's namespace

    patron = models.ForeignKey('Patron', verbose_name=_("patron"), related_name='payments')
    month = models.DateField(_("month"))
    reward = models.ForeignKey('Reward', verbose_name=_("reward"), related_name='+')
    pledge = models.DecimalField(_("pledge"), max_digits=8, decimal_places=2)
    status = models.CharField(_("status"), max_length=12, choices=STATUS.choices, default=STATUS.PROCESSED)
    completed = models.BooleanField(_("completed"), default=False)

    objects = PaymentQuerySet.as_manager()

    class Meta:
        verbose_name = _("payment")
        verbose_name_plural = _("payments")
        unique_together = (
            ('patron', 'month'),
        )

    def get_month_display(self):
        return self.month.strftime('%B %Y')
