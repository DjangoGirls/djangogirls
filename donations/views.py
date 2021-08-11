import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import StripeForm

stripe.api_key = settings.STRIPE_SECRET_KEY


def index(request):
    return render(
        request,
        'donations/index.html',
        {
            'form': StripeForm(),
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
        }
    )


def charge(request):
    if request.method == 'POST':
        form = StripeForm(request.POST)
        if form.is_valid():
            amount = int(request.POST['amount'])
            currency = request.POST['currency']

            customer = stripe.Customer.create(
                email=request.POST['email'],
                name=request.POST['name'],
                source=request.POST['stripeToken']
            )

            charge = stripe.Charge.create(
                customer=customer,
                amount=amount * 100,
                currency=currency,
                description="Donation"
            )
            return redirect(
                reverse(
                    'donations:success',
                    kwargs={
                        'amount': amount,
                        'currency': currency
                    }
                )
            )

        return redirect(reverse('donations:error'))


def success(request, currency, amount):
    currency_symbol = {
        'gbp': '£',
        'eur': '€',
        'usd': '$',
    }

    return render(
        request,
        'donations/success.html',
        {
            'amount': amount,
            'currency': currency_symbol[currency]
        }
    )


def error(request):
    return render(request, 'donations/error.html')
