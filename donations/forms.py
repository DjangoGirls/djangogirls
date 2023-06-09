from django import forms


class StripeForm(forms.Form):
    """Form for handling stripe donations"""

    DONATION_CHOICES = (
        ("10", "10"),
        ("25", "25"),
        ("50", "50"),
        ("100", "100"),
    )
    CURRENCY_CHOICES = (
        ("usd", "$ (US dollars)"),
        ("eur", "€ (Euro)"),
        ("gbp", "£ (GBP)"),
    )

    currency = forms.ChoiceField(choices=CURRENCY_CHOICES)
    amount = forms.ChoiceField(choices=DONATION_CHOICES)
    email = forms.EmailField()
    name = forms.CharField()
