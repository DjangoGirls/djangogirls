import os

import pytest
from django.test import override_settings
from django.urls import reverse
from pytest_django.asserts import assertContains
from stripe.error import StripeError

STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY", "test_public")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "test_public")


def test_index_no_stripe_keys(client):
    with override_settings(STRIPE_PUBLIC_KEY=None, STRIPE_SECRET_KEY=None):
        # Access donations
        resp = client.get(reverse("donations:index"))
        assert resp.status_code == 200

        # Check if it returns a list of past and future events
        assert "form" and "STRIPE_PUBLIC_KEY" not in resp.context


def test_index(client):
    with override_settings(STRIPE_PUBLIC_KEY=STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY=STRIPE_SECRET_KEY):
        resp = client.get(reverse("donations:index"))
        assert resp.status_code == 200

        # Check if it returns a list of past and future events
        assert "form" and "STRIPE_PUBLIC_KEY" in resp.context


def test_charge_get(client):
    resp = client.get(reverse("donations:charge"))
    assert resp.status_code == 403


def test_charge_post(client):
    with override_settings(STRIPE_PUBLIC_KEY=STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY=STRIPE_SECRET_KEY):
        charge_data = {"name": "Paul Smith", "email": "paul.smith@djangogirls.org", "currency": "usd", "amount": "5"}
        # This is missing stripe data
        resp = client.post(reverse("donations:charge"), data=charge_data)
        assert resp.status_code == 302
        assert resp["Location"] == reverse("donations:error")


def test_charge_post_invalid_keys(client):
    with override_settings(STRIPE_PUBLIC_KEY=STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY=STRIPE_SECRET_KEY):
        charge_data = {
            "name": "Paul Smith",
            "email": "paul.smith@djangogirls.org",
            "currency": "usd",
            "amount": "10",
            "stripeToken": "test_code",
        }
        with pytest.raises(StripeError):
            # This is missing stripe data
            client.post(reverse("donations:charge"), data=charge_data)


def test_sponsors(client, globalpartner, globalpartner2):
    resp = client.get(reverse("donations:sponsors"))
    assert resp.status_code == 200
    assertContains(resp, "Django Software Foundation")
    assertContains(resp, "Caktus Group")
