from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from django_date_extensions.fields import ApproximateDate


def test_index(client, future_event, past_event, global_partners):
    # Access homepage
    resp = client.get(reverse("core:index"))
    assert resp.status_code == 200

    # Check if it returns a list of past and future events
    assert "past_events" and "future_events" in resp.context

    # Check if it returns global_partners lists
    assert "platinum" and "diamond" in resp.context
    assert "gold" and "silver" in resp.context
    assert "bronze" in resp.context

    # Only the future event is on the list
    event_ids = {event.pk for event in resp.context["future_events"]}
    assert event_ids == {future_event.pk}


def test_event_published(client, future_event, past_event):
    url1 = reverse("core:event", kwargs={"page_url": future_event.page_url})
    resp_1 = client.get(url1)
    assert resp_1.status_code == 200

    # Check if it's possible to access the page
    url2 = reverse("core:event", kwargs={"page_url": past_event.page_url})
    resp_2 = client.get(url2)
    assert resp_2.status_code == 200

    # Check if website is returning correct data
    assert "page" and "menu" and "content" in resp_1.context
    assert "page" and "menu" and "content" in resp_2.context

    # Check if not public content is not available in context:
    assert future_event.pk not in {content.pk for content in resp_1.context["content"]}


def test_event_unpublished(client, hidden_event):
    # Check if accessing unpublished page renders the event_not_live page
    url = reverse("core:event", kwargs={"page_url": hidden_event.page_url})
    resp = client.get(url)
    assert resp.status_code == 200

    # Check if website is returning correct data
    assert "city" and "past" in resp.context


def test_event_path(client, diff_url_event):
    # Ensure new url path for event view works
    url = reverse("core:event", kwargs={"page_url": diff_url_event.page_url})
    resp = client.get(url)
    assert resp.status_code == 200

    # Check if website is returning correct data
    assert "city" and "past" in resp.context


def test_event_live(client, future_event):
    # Ensure new url path for event view works
    url = reverse("core:event", kwargs={"page_url": future_event.page_url})
    resp = client.get(url)
    assert resp.status_code == 200

    # Check if website is returning correct data
    assert "event" and "menu" and "content" in resp.context


def test_event_city(client, diff_url_event):
    # Ensure old use of City in the url 404s when the slug is different
    url = reverse("core:event", kwargs={"page_url": diff_url_event.city})
    resp = client.get(url)
    assert resp.status_code == 404


def test_event_unpublished_with_future_and_past_dates(client, no_date_event):
    future_date = timezone.now() + timedelta(days=1)
    past_date = timezone.now() - timedelta(days=1)

    # make the event date in the future
    no_date_event.date = ApproximateDate(year=future_date.year, month=future_date.month, day=future_date.day)
    no_date_event.save()

    # Check if accessing unpublished page renders the event_not_live page
    url = reverse("core:event", kwargs={"page_url": no_date_event.page_url})
    resp = client.get(url)
    assert resp.status_code == 200

    # Check if website is returning correct content
    assert "will be coming soon" in str(resp.content)

    # make the event date in the past
    no_date_event.date = ApproximateDate(year=past_date.year, month=past_date.month, day=past_date.day)
    no_date_event.save()

    # Check if accessing unpublished page renders the event_not_live page
    url = reverse("core:event", kwargs={"page_url": no_date_event.page_url})
    resp = client.get(url)
    assert resp.status_code == 200

    # Check if website is returning correct content
    assert "has already happened" in str(resp.content)


def test_event_unpublished_with_auth_normal(user, client, hidden_event):
    """Test that an unpublished page can not be accessed when the user is
    authenticated and not a superuser"""

    client.force_login(user)
    url = reverse("core:event", kwargs={"page_url": hidden_event.page_url})
    resp = client.get(url)

    assert resp.status_code == 200
    assert "city" and "past" in resp.context


def test_event_unpublished_with_auth_superuser(admin_client, hidden_event):
    """Test that an unpublished page can be accessed when the user is
    authenticated and a superuser"""

    url = reverse("core:event", kwargs={"page_url": hidden_event.page_url})
    resp = admin_client.get(url)

    assert resp.status_code == 200
    assert hidden_event.page_title in resp.content.decode("utf-8")


def test_event_unpublished_with_auth_not_organizer(user, client, hidden_event):
    """Test that an unpublished page can not be accessed if the user
    is not an organizer"""

    client.force_login(user)
    url = reverse("core:event", kwargs={"page_url": hidden_event.page_url})
    resp = client.get(url)

    assert resp.status_code == 200
    assert "city" and "past" in resp.context


def test_event_unpublished_with_auth_in_team(user, client, hidden_event):
    """Test that an unpublished page can be accessed if the user
    is an organizer"""
    hidden_event.team.add(user)

    client.force_login(user)
    url = reverse("core:event", kwargs={"page_url": hidden_event.page_url})
    resp = client.get(url)

    assert resp.status_code == 200
    assert hidden_event.page_title in resp.content.decode("utf-8")


def test_event_unpublished_with_auth_organizer(user, client, hidden_event):
    """Test that an unpublished page can be accessed if the user
    is the main organizer"""
    hidden_event.main_organizer = user

    client.force_login(user)
    url = reverse("core:event", kwargs={"page_url": hidden_event.page_url})
    resp = client.get(url)

    assert resp.status_code == 200
    assert hidden_event.page_title in resp.content.decode("utf-8")


def test_event_multiple_events_same_page_url(client, future_event, old_event):
    # Check if event loads even if a past event has same page_url
    url = reverse("core:event", kwargs={"page_url": future_event.page_url})
    resp = client.get(url)
    assert resp.status_code == 200

    # Check if website is returning correct data
    assert "event" and "menu" and "content" in resp.context


def test_coc_legacy(client):
    AVAILABLE_LANG = {
        "en": "<h1>Code of Conduct</h1>",
        "es": "<h1>Código de Conducta</h1>",
        "fr": "<h1>Code de Conduite</h1>",
        "ko": "<h1>준수 사항</h1>",
        "pt-br": "<h1>Código de Conduta</h1>",
    }
    for lang, title in AVAILABLE_LANG.items():
        response = client.get(f"/coc/{lang}/")
        assert title in response.content.decode("utf-8"), title


def test_coc_no_lang(client):
    title = "<h1>Code of Conduct</h1>"

    response = client.get("/coc/")
    assert title in response.content.decode("utf-8"), title


def test_coc_invalid_lang(client):
    response = client.get("/coc/pl/")
    assert response.status_code == 404


def test_coc(client):
    url = reverse("core:coc")
    response = client.get(url)
    assert response.status_code == 200


def test_events(client):
    url = reverse("core:events")
    response = client.get(url)
    assert response.status_code == 200


def test_events_map(client):
    url = reverse("core:events_map")
    response = client.get(url)
    assert response.status_code == 200


def test_resources(client):
    url = reverse("core:resources")
    response = client.get(url)
    assert response.status_code == 200


def test_events_icalendar_no_events(client):
    url = reverse("core:icalendar")
    response = client.get(url)
    assert response.status_code == 200


def test_events_icalendar_events(client, events):
    url = reverse("core:icalendar")
    response = client.get(url)
    assert response.status_code == 200


def test_newsletter(client):
    url = reverse("core:newsletter")
    response = client.get(url)
    assert response.status_code == 200


def test_faq(client):
    url = reverse("core:faq")
    response = client.get(url)
    assert response.status_code == 200


def test_foundation(client):
    url = reverse("core:foundation")
    response = client.get(url)
    assert response.status_code == 200


def test_foundation_gov_doc(client):
    url = reverse("core:foundation-governing-document")
    response = client.get(url)
    assert response.status_code == 200


def test_year_2015(client):
    url = reverse("core:year_2015")
    response = client.get(url)
    assert response.status_code == 200


def test_year_2016_17(client):
    url = reverse("core:year_2016_2017")
    response = client.get(url)
    assert response.status_code == 200


def test_terms(client):
    url = reverse("core:terms-conditions")
    response = client.get(url)
    assert response.status_code == 200


def test_privacy_cookies(client):
    url = reverse("core:privacy-cookies")
    response = client.get(url)
    assert response.status_code == 200


def test_server_error(client):
    url = reverse("core:server_error")
    response = client.get(url)
    assert response.status_code == 500


# Disabling this due to test requiring redirects to exist in flatpages (database content)
# def test_coc_redirect(client):
#     REDIRECTS = {
#         'coc/': '/coc/',
#         'coc-es-la/': '/coc/es/',
#         'coc-fr/': '/coc/fr/',
#         'coc-kr/': '/coc/ko/',
#         'coc-pt-br/': '/coc/pt-br/',
#         'coc/rec/': '/coc/pt-br/',
#     }
#     for old_url_name, new_url in REDIRECTS.items():
#         old_url = reverse('django.contrib.flatpages.views.flatpage', args=[old_url_name])
#         resp = client.get(old_url)
#         assert resp.status_code == 301
#         assert resp['Location'] == new_url


def test_contribute(client):
    url = reverse("core:contribute")
    resp = client.get(url)
    assert resp.status_code == 200


"""
def test_crowdfunding_donors(client, visible_donors, hidden_donors):
    # Access crowdfunding donors page
    resp = client.get(reverse('core:crowdfunding-donors'))
    assert resp.status_code == 200

    # Check if it returns list of donors in response
    donor_list = set(visible_donors)
    assert donor_list == set(resp.context['donor_list'])

    # Only the visible donors
    donor_ids = set(donor.pk for donor in resp.context['donor_list'])
    visible_donors = set(visible_donor.pk for visible_donor in visible_donors)
    assert donor_ids == visible_donors
"""


def test_robots_txt_view(client):
    response = client.get(reverse("core:robots"))
    assert response.status_code == 200
