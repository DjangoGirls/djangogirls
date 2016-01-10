from django.core.urlresolvers import reverse
from django.test import TestCase

from applications.utils import get_organiser_menu


class MenuTest(TestCase):
    def test_organiser_menu_entries(self):
        menu = get_organiser_menu('london')
        self.assertEqual(menu[0]['url'], '/london/applications/')
        self.assertEqual(menu[1]['url'], '/london/communication/')
        self.assertEqual(menu[2]['url'], '/london/coach_applications/')
        self.assertEqual(menu[3]['url'], '/london/coach_communication/')
