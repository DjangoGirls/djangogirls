from core.forms import AddOrganizerForm


def test_name_splitting(future_event):
    form = AddOrganizerForm({"event": future_event.pk, "email": "olaf@djangogirls.org", "name": "Olaf Olaffson"})

    assert form.is_valid()
    organizer = form.save()
    assert organizer.first_name == "Olaf"
    assert organizer.last_name == "Olaffson"
