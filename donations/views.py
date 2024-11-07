import uuid

import stripe
from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse
from stripe.error import APIConnectionError, CardError, StripeError

from patreonmanager.models import FundraisingStatus
from stripe_payments.models import StripeCharge

from .forms import StripeForm

stripe.api_key = settings.STRIPE_SECRET_KEY


def index(request):
    context = {
        "patreon_stats": FundraisingStatus.objects.first(),  # TODO: This isn't used
    }
    return render(request, "donations/corporate_sponsorships.html", context)


def donate(request):
    context = {
        "patreon_stats": FundraisingStatus.objects.first(),  # TODO: This isn't used
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
            key = uuid.uuid4().hex
            try:
                customer = stripe.Customer.create(
                    email=request.POST["email"],
                    name=request.POST["name"],
                    source=request.POST.get("stripeToken"),
                    idempotency_key=key,
                )
            except APIConnectionError as err:
                request.session["stripe_message"] = err.user_message
                return redirect(reverse("donations:error"))
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


def crowdfunding(request):
    total_raised = StripeCharge.objects.running_total()["total"]
    recent_donors = StripeCharge.objects.all().order_by("-charge_created")[:10]
    return render(request, "donations/crowdfunding.html", {"total_raised": total_raised, "donors": recent_donors})
