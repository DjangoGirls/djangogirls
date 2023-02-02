from django.urls import reverse


def test_add_globalpartner_superuser(admin_client):
    response = admin_client.get(reverse("admin:globalpartners_globalpartner_add"))
    assert response.status_code == 200


def test_edit_globalpartner_superuser(admin_client, globalpartner, global_partner_data):
    response = admin_client.get(reverse("admin:globalpartners_globalpartner_change", args=(globalpartner.pk,)))
    assert response.status_code == 200
    response = admin_client.post(
        reverse("admin:globalpartners_globalpartner_change", args=(globalpartner.pk,)), data=global_partner_data
    )
    assert response.status_code == 302


def test_view_globalpartners_superuser(admin_client):
    response = admin_client.get(reverse("admin:globalpartners_globalpartner_changelist"))
    assert response.status_code == 200


def test_globalpartners_globalpartner_send_prospective_sponsor_email(admin_client, globalpartner):
    response = admin_client.post(
        reverse("admin:globalpartners_globalpartner_send_prospective_sponsor_email", args=(globalpartner.pk,))
    )
    assert response.status_code == 302


def test_globalpartners_globalpartner_send_renewal_email(admin_client, globalpartner):
    response = admin_client.post(
        reverse("admin:globalpartners_globalpartner_send_renewal_email", args=(globalpartner.pk,))
    )
    assert response.status_code == 302


def test_globalpartners_globalpartner_send_promotional_material_email(admin_client, globalpartner):
    response = admin_client.post(
        reverse("admin:globalpartners_globalpartner_send_promotional_material_email", args=(globalpartner.pk,))
    )
    assert response.status_code == 302


def test_globalpartners_globalpartner_send_thank_you_email(admin_client, globalpartner):
    response = admin_client.post(
        reverse("admin:globalpartners_globalpartner_send_thank_you_email", args=(globalpartner.pk,))
    )
    assert response.status_code == 302


"""Tests to make sure only superusers can manage globalpartners and organizers have no
access to this module."""


def test_add_globalpartner_organizer(user_client):
    response = user_client.get(reverse("admin:globalpartners_globalpartner_add"))
    assert response.status_code == 302


def test_edit_globalpartner_organizer(user_client, globalpartner):
    response = user_client.get(reverse("admin:globalpartners_globalpartner_change", args=(globalpartner.pk,)))
    assert response.status_code == 302


def test_view_globalpartners_organizer(user_client):
    response = user_client.get(reverse("admin:globalpartners_globalpartner_changelist"))
    assert response.status_code == 302
