from django.test import TestCase

from ..utils import download


class DownloadTestCase(TestCase):
    def test_get_hid_from_proper_url(self):
        test_url = 'http://whatever.info/?hid=whatever'
        hid = download._get_hid_from_url(test_url)
        assert hid == ['whatever']

    def test_get_hid_from_broken_url(self):
        test_url = 'http://whatever.info/?hied=whatever'
        hid = download._get_hid_from_url(test_url)
        assert hid is None

    def test_full_url(self):
        url = 'http://whatever.info'
        params = {'hid': ['whatever']}
        full_url = download._get_full_url(url, params)
        assert full_url == 'http://whatever.info/?hid=whatever'
