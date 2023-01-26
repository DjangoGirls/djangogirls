import io
import random

import requests
from django.conf import settings
from django.core.files.images import ImageFile


def get_flickr_photo_list():
    try:
        req = requests.get(
            "https://www.flickr.com/services/rest/"
            "?method=flickr.people.getPublicPhotos"
            f"&api_key={settings.FLICKR_API_KEY}"
            f"&user_id={settings.FLICKR_DJANGO_GIRLS_USER_ID}"
            "&extras=o_dims&format=json&nojsoncallback=1"
        )
        return req.json()
    except requests.exceptions.RequestException:
        return None


def filter_landscape_photos(json_response):
    try:
        photo_list = json_response["photos"]["photo"]
        return [photo for photo in photo_list if (photo["o_width"] > photo["o_height"])]
    except (TypeError, KeyError):
        return None


def get_random_photo_selection(photo_list, amount_to_select):
    try:
        return random.sample(photo_list, k=amount_to_select)
    except (TypeError, ValueError):
        return None


def get_photo_files(photo_list):
    photo_files_list = []
    try:
        for photo in photo_list:
            request = requests.get(
                f'https://live.staticflickr.com/{photo["server"]}/' f'{photo["id"]}_{photo["secret"]}_b.jpg'
            )
            photo_file = ImageFile(io.BytesIO(request.content), name=f'{photo["id"]}.jpg')
            photo_files_list.append(photo_file)
        return photo_files_list if len(photo_files_list) else None
    except (requests.exceptions.RequestException, TypeError, KeyError):
        return None


def select_random_flickr_photos(amount_to_select):
    photo_list = get_flickr_photo_list()
    only_lanscape_photo_list = filter_landscape_photos(photo_list)
    only_landscape_random_selection = get_random_photo_selection(only_lanscape_photo_list, amount_to_select)
    return get_photo_files(only_landscape_random_selection)
