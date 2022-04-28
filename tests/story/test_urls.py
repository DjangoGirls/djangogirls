from django.urls import reverse


def test_blog_sitemap_url(client, blog_posts):
    response = client.get(reverse('story:sitemap'))
    assert response.status_code == 200
