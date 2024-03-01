from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

today = date.today()


def validate_approximatedate(e_date):
    if e_date.month == 0:
        raise ValidationError(_("Event date can't be a year only. " "Please, provide at least a month and a year."))
    if e_date.day == 0:
        raise ValidationError(_("Please enter a valid date, which is at least 3 months (90 days) from now."))


def validate_event_date(e_date):
    if date(e_date.year, e_date.month, e_date.day) - today < timedelta(days=90):
        raise ValidationError(
            _("Your event date is too close. " "Workshop date should be at least 3 months (90 days) from now.")
        )


def validate_future_date(e_date):
    if date(e_date.year, e_date.month, e_date.day) - today < timedelta(days=0):
        raise ValidationError(_("Event date should be in the future"))
