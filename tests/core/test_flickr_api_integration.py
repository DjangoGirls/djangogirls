from unittest import mock

import requests

from core.flickr_api_integration import (
    filter_landscape_photos,
    get_flickr_photo_list,
    get_photo_files,
    get_random_photo_selection,
)


@mock.patch("requests.get")
def test_get_flickr_photo_list_when_json_returned(mock_get):
    mock_get.return_value.json.return_value = {"photos": {}, "stat": "ok"}

    result = get_flickr_photo_list()

    assert result == {"photos": {}, "stat": "ok"}


@mock.patch("requests.get")
def test_get_flickr_photo_list_when_bad_request(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException

    result = get_flickr_photo_list()

    assert result is None


def test_filter_landscape_photos_when_dict_has_photos():
    sample_photo_object = {
        "photos": {
            "page": 1,
            "pages": 192,
            "perpage": 100,
            "total": 19190,
            "photo": [
                {
                    "id": "49955170588",
                    "owner": "128162583@N08",
                    "secret": "c6fcd9f6d8",
                    "server": "65535",
                    "farm": 66,
                    "title": "_MG_5772",
                    "ispublic": 1,
                    "isfriend": 0,
                    "isfamily": 0,
                    "o_width": "4882",
                    "o_height": "2888",
                },
                {
                    "id": "49956011912",
                    "owner": "128162583@N08",
                    "secret": "13e1098854",
                    "server": "65535",
                    "farm": 66,
                    "title": "_MG_5367",
                    "ispublic": 1,
                    "isfriend": 0,
                    "isfamily": 0,
                    "o_width": "3456",
                    "o_height": "5184",
                },
                {
                    "id": "49955956852",
                    "owner": "128162583@N08",
                    "secret": "10fe590daa",
                    "server": "65535",
                    "farm": 66,
                    "title": "_MG_5763",
                    "ispublic": 1,
                    "isfriend": 0,
                    "isfamily": 0,
                    "o_width": "3672",
                    "o_height": "2354",
                },
                {
                    "id": "49955684711",
                    "owner": "128162583@N08",
                    "secret": "612c5f96a1",
                    "server": "65535",
                    "farm": 66,
                    "title": "_MG_5393",
                    "ispublic": 1,
                    "isfriend": 0,
                    "isfamily": 0,
                    "o_width": "3456",
                    "o_height": "5184",
                },
                {
                    "id": "49955674596",
                    "owner": "128162583@N08",
                    "secret": "bb357b3728",
                    "server": "65535",
                    "farm": 66,
                    "title": "_MG_5759",
                    "ispublic": 1,
                    "isfriend": 0,
                    "isfamily": 0,
                    "o_width": "4632",
                    "o_height": "2141",
                },
            ],
        },
        "stat": "ok",
    }

    sample_photo_object_result = [
        {
            "id": "49955170588",
            "owner": "128162583@N08",
            "secret": "c6fcd9f6d8",
            "server": "65535",
            "farm": 66,
            "title": "_MG_5772",
            "ispublic": 1,
            "isfriend": 0,
            "isfamily": 0,
            "o_width": "4882",
            "o_height": "2888",
        },
        {
            "id": "49955956852",
            "owner": "128162583@N08",
            "secret": "10fe590daa",
            "server": "65535",
            "farm": 66,
            "title": "_MG_5763",
            "ispublic": 1,
            "isfriend": 0,
            "isfamily": 0,
            "o_width": "3672",
            "o_height": "2354",
        },
        {
            "id": "49955674596",
            "owner": "128162583@N08",
            "secret": "bb357b3728",
            "server": "65535",
            "farm": 66,
            "title": "_MG_5759",
            "ispublic": 1,
            "isfriend": 0,
            "isfamily": 0,
            "o_width": "4632",
            "o_height": "2141",
        },
    ]

    result = filter_landscape_photos(sample_photo_object)

    assert result == sample_photo_object_result


def test_filter_landscape_photos_when_dict_no_photos():
    result = filter_landscape_photos(
        {"stat": "fail", "code": 112, "message": "Method 'flickr.people.getPublicPhtos' not found"}
    )

    assert result is None


def test_filter_landscape_photos_when_empty_dict():
    result = filter_landscape_photos({})

    assert result is None


def test_filter_landscape_photos_when_string_passed():
    result = filter_landscape_photos("some value")

    assert result is None


def test_filter_landscape_photos_when_int_passed():
    result = filter_landscape_photos(7)

    assert result is None


def test_filter_landscape_photos_when_none_passed():
    result = filter_landscape_photos(None)

    assert result is None


@mock.patch("random.sample")
def test_get_random_photo_selection_when_list_present(mock_library):
    get_random_photo_selection([], 2)

    assert mock_library.called


def test_get_random_photo_selection_when_list_empty():
    result = get_random_photo_selection([], 2)

    assert result is None


def test_get_random_photo_selection_when_string_passed():
    result = get_random_photo_selection("", 2)

    assert result is None


def test_get_random_photo_selection_when_none_passed():
    result = get_random_photo_selection(None, 2)

    assert result is None


def test_get_random_photo_selection_when_int_passed():
    result = get_random_photo_selection(2, 2)

    assert result is None


@mock.patch("io.BytesIO")
@mock.patch("core.flickr_api_integration.ImageFile")
@mock.patch("requests.get")
def test_get_photo_files_when_image_returned(mock_get, mock_image_file, mock_bytes_io):
    mock_get.return_value.content = b"some initial binary data: \x00\x01"
    mock_bytes_io.return_value = b"\x00\x01"

    result = get_photo_files(
        [
            {
                "id": "49955674596",
                "owner": "128162583@N08",
                "secret": "bb357b3728",
                "server": "65535",
                "farm": 66,
                "title": "_MG_5759",
                "ispublic": 1,
                "isfriend": 0,
                "isfamily": 0,
                "o_width": "4632",
                "o_height": "2141",
            }
        ]
    )

    mock_bytes_io.assert_called_once_with(b"some initial binary data: \x00\x01")
    mock_image_file.assert_called_once_with(b"\x00\x01", name="49955674596.jpg")

    assert isinstance(result, list)
    assert len(result) == 1


@mock.patch("requests.get")
def test_get_photo_files_when_bad_request(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException

    result = get_photo_files(
        [
            {
                "id": "49955674596",
                "owner": "128162583@N08",
                "secret": "bb357b3728",
                "server": "65535",
                "farm": 66,
                "title": "_MG_5759",
                "ispublic": 1,
                "isfriend": 0,
                "isfamily": 0,
                "o_width": "4632",
                "o_height": "2141",
            }
        ]
    )

    assert result is None


def test_get_photo_files_when_empty_object():

    result = get_photo_files([{}])

    assert result is None


def test_get_photo_files_when_dict_passed():

    result = get_photo_files({})

    assert result is None


def test_get_photo_files_when_string_passed():

    result = get_photo_files("some string")

    assert result is None


def test_get_photo_files_when_int_passed():

    result = get_photo_files(3)

    assert result is None


def test_get_photo_files_when_none_passed():

    result = get_photo_files(None)

    assert result is None
