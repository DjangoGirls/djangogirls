def test_stripe_charge_model_str_presentation(donation):
    assert str(donation) == donation.charge_id
