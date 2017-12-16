from applications.questions import get_organiser_menu


def test_organiser_menu_entries():
    menu = get_organiser_menu('london')
    assert menu[0]['url'] == '/london/applications/'
    assert menu[1]['url'] == '/london/communication/'
