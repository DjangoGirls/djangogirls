from django.test import TestCase
from applications.utils import get_organiser_menu


class MenuTest(TestCase):
    def test_menu_entries(self):
        menu = get_organiser_menu('london')
        self.assertEqual(menu[0]['url'], 'applications/')
        self.assertEqual(menu[1]['url'], 'communication/')
