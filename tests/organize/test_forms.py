from organize.forms import RemoteWorkshopForm, WorkshopForm


def test_workshop_remote_form_valid_date(workshop_remote_form_valid_date):
    form = RemoteWorkshopForm(data=workshop_remote_form_valid_date)
    assert form.is_valid()
    assert form.errors == {}


def test_workshop_remote_form_date_too_close(workshop_remote_form_date_too_close):
    form = RemoteWorkshopForm(data=workshop_remote_form_date_too_close)
    assert not form.is_valid()
    assert form.errors["date"] == [
        "Your event date is too close. Workshop date should be at least 3 months (90 days) from now."
    ]


def test_workshop_remote_form_date_in_the_past(workshop_remote_form_past_date):
    form = RemoteWorkshopForm(data=workshop_remote_form_past_date)
    assert not form.is_valid()
    assert form.errors["date"] == ["Event date should be in the future"]


def test_workshop_remote_form_date_year_only(workshop_remote_form_date_year_only):
    form = RemoteWorkshopForm(data=workshop_remote_form_date_year_only)
    assert not form.is_valid()
    assert form.errors["date"] == ["Event date can't be a year only. Please, provide at least a month and a year."]


def test_workshop_form_valid_date(workshop_form_valid_date):
    form = WorkshopForm(data=workshop_form_valid_date)
    assert form.is_valid()
    assert form.errors == {}


def test_workshop_form_date_too_close(workshop_form_too_close):
    form = WorkshopForm(data=workshop_form_too_close)
    assert not form.is_valid()
    assert form.errors["date"] == [
        "Your event date is too close. Workshop date should be at least 3 months (90 days) from now."
    ]


def test_workshop_form_date_in_the_past(workshop_form_past_date):
    form = WorkshopForm(data=workshop_form_past_date)
    assert not form.is_valid()
    assert form.errors["date"] == ["Event date should be in the future"]


def test_workshop_form_date_year_only(workshop_form_date_year_only):
    form = WorkshopForm(data=workshop_form_date_year_only)
    assert not form.is_valid()
    assert form.errors["date"] == ["Event date can't be a year only. Please, provide at least a month and a year."]
