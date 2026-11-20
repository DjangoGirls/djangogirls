from django.urls import reverse


def test_stock_picture_add_page(admin_client):
    # The photo credit help text is a lazy, HTML-safe translation: it must render as a string
    response = admin_client.get(reverse("admin:pictures_stockpicture_add"))

    assert response.status_code == 200
    assert "creativecommons.org/licenses/" in response.content.decode()
