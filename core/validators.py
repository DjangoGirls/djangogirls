from datetime import date, datetime, timedelta

from django.core.exceptions import ValidationError


def validate_approximatedate(date):
    if date.month == 0:
        raise ValidationError(
            'Event date can\'t be a year only. '
            'Please, provide at least a month and a year.'
        )


def validate_event_date(e_date):
    today = date.today()
    event_date = datetime.date(datetime.strptime('{0}-{1}-{2}'.format(e_date.year, e_date.month, e_date.day),
                                                 '%Y-%m-%d'))
    if event_date - today < timedelta(days=90):
        raise ValidationError('Your event date is too close. '
                              'Workshop date should be at least 3 months (90 days) from now.')
