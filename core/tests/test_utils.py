from unittest import TestCase
from mock import patch

from core.utils import get_coordinates_for_city, NOMINATIM_URL


@patch('requests.get')
class GetCoordinatesForCityTest(TestCase):
    def test_get_coordinates_for_city(self, mock_get):
        mock_get.return_value.json.return_value = [{
            'lat': '1.23',
            'lon': '4.56',
        }]

        result = get_coordinates_for_city('London', 'UK')

        mock_get.assert_called_once_with(
            NOMINATIM_URL,
            params={
                'format': 'json',
                'q': 'London, UK',
            }
        )
        self.assertEqual(result, '1.23, 4.56')

    def test_returns_none_when_no_results(self, mock_get):
        # Results are an empty list
        mock_get.return_value.json.return_value = []

        result = get_coordinates_for_city('PretendTown', 'UK')

        mock_get.assert_called_once_with(
            NOMINATIM_URL,
            params={
                'format': 'json',
                'q': 'PretendTown, UK',
            }
        )
        self.assertIsNone(result)

    def test_returns_none_when_invalid_results(self, mock_get):
        # Empty dict returned in results
        mock_get.return_value.json.return_value = [{}]

        result = get_coordinates_for_city('PretendTown', 'UK')

        mock_get.assert_called_once_with(
            NOMINATIM_URL,
            params={
                'format': 'json',
                'q': 'PretendTown, UK',
            }
        )
        self.assertIsNone(result)
