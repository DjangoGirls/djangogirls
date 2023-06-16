import stripe
from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse
from stripe.error import CardError, StripeError

from patreonmanager.models import FundraisingStatus

from .forms import StripeForm

stripe.api_key = settings.STRIPE_SECRET_KEY


def index(request):
    context = {
        "patreon_stats": FundraisingStatus.objects.all().first(),  # TODO: This isn't used
    }
    if settings.STRIPE_PUBLIC_KEY:
        context.update({"form": StripeForm(), "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY})
    return render(request, "donations/donate.html", context)


def charge(request):
    if request.method == "POST":
        form = StripeForm(request.POST)
        if form.is_valid():
            amount = int(request.POST["amount"])
            currency = request.POST["currency"]

            try:
                customer = stripe.Customer.create(
                    email=request.POST["email"], name=request.POST["name"], source=request.POST["stripeToken"]
                )
            except CardError as err:
                request.session["stripe_message"] = err.user_message
                return redirect(reverse("donations:error"))
            try:
                stripe.Charge.create(customer=customer, amount=amount * 100, currency=currency, description="Donation")
            except StripeError as err:
                request.session["stripe_message"] = err.user_message
                return redirect(reverse("donations:error"))
            else:
                return redirect(reverse("donations:success", kwargs={"amount": amount, "currency": currency}))
        return redirect(reverse("donations:error"))

    else:
        return HttpResponseForbidden()


def success(request, currency, amount):
    currency_symbol = {
        "gbp": "£",
        "eur": "€",
        "usd": "$",
    }

    return render(request, "donations/success.html", {"amount": amount, "currency": currency_symbol[currency]})


def error(request):
    if "stripe_message" in request.session:
        error_message = request.session.get("stripe_message")
        del request.session["stripe_message"]

    return render(request, "donations/error.html", {"stripe_message": error_message})


def sponsors(request):
    return render(request, "donations/sponsors.html")
