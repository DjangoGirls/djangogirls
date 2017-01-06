from django.core.exceptions import ValidationError


def validate_approximatedate(date):
    if date.month == 0:
        raise ValidationError(
            'Event date can\'t be a year only. '
            'Please, provide at least a month and a year.'
        )
