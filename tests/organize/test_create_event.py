EVENT_FIELDS = ["date", "city", "country", "latlng"]


def test_create_event(base_application, stock_pictures):
    event = base_application.create_event()

    # we explicitly list the name of fields below, instead of using
    # getattr, to make the tests more beginners-friendly
    assert event.date == base_application.date
    assert event.city == base_application.city
    assert event.country == base_application.country
    assert event.latlng == base_application.latlng
    assert event.page_url == base_application.website_slug

    name = f"Django Girls {event.city}"
    email = f"{event.page_url}@djangogirls.org"
    assert event.name == name
    assert event.page_title == name
    assert event.email == email

    # check that we populate content from default event
    expected_content_sections = ["about", "values", "apply", "faq", "coach", "partners", "footer"]
    event_content_sections = [e.name for e in event.content.all()]
    assert set(event_content_sections) == set(expected_content_sections)

    # check that we populate menu from default event
    assert event.menu.count() > 0
    expected_menu_items = ["About", "Apply for a pass!", "FAQ", "Become a coach", "Partners"]
    event_menu_items = [e.title for e in event.menu.all()]
    assert set(event_menu_items) == set(expected_menu_items)

    # check that we add a cover pictures
    assert event.photo is not None
    assert event.photo_credit is not None
    assert event.photo_link is not None
