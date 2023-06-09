def test_get_rsvp_link(email, event):
    link = email.get_rsvp_link("abcd")
    assert "abcd" in link
    assert event.page_url in link


def test_add_rsvp_links(accepted_application, email):
    assert "[rsvp-url-yes]" in email.text
    assert "[rsvp-url-no]" in email.text
    body = email.add_rsvp_links(email.text, accepted_application)

    assert accepted_application.get_rsvp_yes_code() in body
    assert accepted_application.get_rsvp_no_code() in body
    assert "[rsvp-url-yes]" not in body
    assert "[rsvp-url-no]" not in body


def test_send(accepted_application, email):
    email.send()

    assert email.number_of_recipients == 1
    assert email.successfuly_sent == accepted_application.email
