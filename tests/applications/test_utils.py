from django.utils.translation import activate

from applications.questions import get_organiser_menu


def test_organiser_menu_entries_en():
    activate("en")  # default language, but to be explicit
    menu = get_organiser_menu("london")
    assert menu[0]["url"] == "/en/london/applications/"
    assert menu[1]["url"] == "/en/london/communication/"


def test_organiser_menu_entries_fr():
    activate("fr")  # test french
    menu = get_organiser_menu("london")
    assert menu[0]["url"] == "/fr/london/applications/"
    assert menu[1]["url"] == "/fr/london/communication/"
