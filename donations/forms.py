from django import forms


class StripeForm(forms.Form):
    """ Form for handling stripe donations """

    DONATION_CHOICES = (
        ('10', '10'),
        ('25', '25'),
        ('50', '50'),
        ('100', '100'),
    )
    CURRENCY_CHOICES = (
        ('eur', '€ (Euro)'),
        ('gbp', '£ (GBP)'),
        ('usd', '$ (US dollars)'),
    )

    amount = forms.ChoiceField(choices=DONATION_CHOICES)
    currency = forms.ChoiceField(choices=CURRENCY_CHOICES)
    email = forms.EmailField()
    name = forms.CharField()
