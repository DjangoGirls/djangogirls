from django.urls import reverse


def test_form_thank_you(client):
    # Access the thank you page
    resp = client.get(reverse('organize:form_thank_you'))
    assert resp.status_code == 200


def test_index(client):
    # Access the organize homepage
    resp = client.get(reverse('organize:index'))
    assert resp.status_code == 200


def test_commitment(client):
    # Access the commitment page
    resp = client.get(reverse('organize:commitment'))
    assert resp.status_code == 200


def test_prerequisites(client):
    # Access prerequisites page
    resp = client.get(reverse('organize:prerequisites'))
    assert resp.status_code == 200


def test_suspend(client):
    # Access suspend page
    resp = client.get(reverse('organize:suspend'))
    assert resp.status_code == 200
