from datetime import date
from unittest import mock

from freezegun import freeze_time

from core.utils import NOMINATIM_URL, get_coordinates_for_city, next_deadline


@mock.patch("requests.get")
def test_get_coordinates_for_city(mock_get):
    mock_get.return_value.json.return_value = [
        {
            "lat": "1.23",
            "lon": "4.56",
        }
    ]

    result = get_coordinates_for_city("London", "UK")

    mock_get.assert_called_once_with(
        NOMINATIM_URL,
        params={
            "format": "json",
            "q": "London, UK",
        },
    )
    expected_lat = "{:.7f}".format(float("1.23"))
    expected_lon = "{:.7f}".format(float("4.56"))
    assert result == f"{expected_lat}, {expected_lon}"


@mock.patch("requests.get")
def test_returns_none_when_no_results(mock_get):
    # Results are an empty list
    mock_get.return_value.json.return_value = []

    result = get_coordinates_for_city("PretendTown", "UK")

    mock_get.assert_called_once_with(
        NOMINATIM_URL,
        params={
            "format": "json",
            "q": "PretendTown, UK",
        },
    )
    assert result is None


@mock.patch("requests.get")
def test_returns_none_when_invalid_results(mock_get):
    # Empty dict returned in results
    mock_get.return_value.json.return_value = [{}]

    result = get_coordinates_for_city("PretendTown", "UK")

    mock_get.assert_called_once_with(
        NOMINATIM_URL,
        params={
            "format": "json",
            "q": "PretendTown, UK",
        },
    )
    assert result is None


@freeze_time("2016-10-10")
def test_a_week_before_deadline():
    result = next_deadline()

    assert result == date(2016, 10, 16)


@freeze_time("2016-10-15")
def test_day_before_deadline():
    result = next_deadline()

    assert result == date(2016, 10, 16)


@freeze_time("2016-10-16")  # noqa: F811
def test_day_before_deadline():  # noqa: F811
    result = next_deadline()

    assert result == date(2016, 10, 16)


@freeze_time("2016-10-17")  # noqa: F811
def test_day_before_deadline():  # noqa: F811
    result = next_deadline()

    assert result == date(2016, 10, 30)
