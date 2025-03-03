import random
from functools import lru_cache

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.utils.translation import gettext_lazy as _

from core.flickr_api_integration import select_random_flickr_photos

DEFAULT_BACKGROUND_PHOTOS = {
    "about": [
        settings.STATICFILES_DIRS[0] + "/img/photos/about1.jpg",
        settings.STATICFILES_DIRS[0] + "/img/photos/about2.jpg",
    ],
    "apply": [settings.STATICFILES_DIRS[0] + "/img/photos/apply.jpg"],
    "coach": [
        settings.STATICFILES_DIRS[0] + "/img/photos/coach1.jpg",
        settings.STATICFILES_DIRS[0] + "/img/photos/coach2.jpg",
    ],
    "footer": [
        settings.STATICFILES_DIRS[0] + "/img/photos/footer1.jpg",
        settings.STATICFILES_DIRS[0] + "/img/photos/footer2.jpg",
    ],
}


def get_random_photo(section):
    if section in DEFAULT_BACKGROUND_PHOTOS:
        photos = DEFAULT_BACKGROUND_PHOTOS[section]
        return UploadedFile(open(photos[random.randint(0, len(photos) - 1)], "rb"))
    return None


@lru_cache
def get_four_random_flickr_photos():
    return select_random_flickr_photos(4)


def select_photo(section):
    four_random_flickr_photos = get_four_random_flickr_photos()
    if not four_random_flickr_photos:
        return get_random_photo(section)
    return four_random_flickr_photos.pop(0)


def get_default_eventpage_data():
    return [
        {"name": "about", "is_public": True, "background": select_photo("about"), "template": "default/about.html"},
        {"name": "values", "is_public": True, "template": "default/values.html"},
        {"name": "apply", "is_public": True, "background": select_photo("apply"), "template": "default/apply.html"},
        {"name": "faq", "is_public": True, "template": "default/faq.html"},
        {"name": "coach", "is_public": True, "background": select_photo("coach"), "template": "default/coach.html"},
        {"name": "partners", "is_public": True, "template": "default/partners.html"},
        {"name": "footer", "is_public": True, "background": select_photo("footer"), "template": "default/footer.html"},
    ]


def get_default_menu():
    return [
        {"title": _("About"), "url": "#values"},
        {"title": _("Apply for a pass!"), "url": "#apply"},
        {"title": _("FAQ"), "url": "#faq"},
        {"title": _("Become a coach"), "url": "#coach"},
        {"title": _("Partners"), "url": "#partners"},
    ]
