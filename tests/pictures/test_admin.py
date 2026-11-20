from django.urls import reverse


def test_stock_picture_add_page(admin_client):
    response = admin_client.get(reverse("admin:pictures_stockpicture_add"))

    assert response.status_code == 200
    assert "<a href='https://creativecommons.org/licenses/'>" in response.content.decode()
