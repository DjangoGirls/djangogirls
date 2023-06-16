def test_global_partner_string_representation(globalpartner):
    assert str(globalpartner) == globalpartner.company_name
