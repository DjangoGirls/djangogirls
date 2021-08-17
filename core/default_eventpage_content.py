# -*- encoding: utf-8 -*-
import random

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile


DEFAULT_BACKGROUND_PHOTOS = {
    'about': [
        settings.STATICFILES_DIRS[0] + '/img/photos/about1.jpg',
        settings.STATICFILES_DIRS[0] + '/img/photos/about2.jpg'
    ],
    'apply': [
        settings.STATICFILES_DIRS[0] + '/img/photos/apply.jpg'
    ],
    'coach': [
        settings.STATICFILES_DIRS[0] + '/img/photos/coach1.jpg',
        settings.STATICFILES_DIRS[0] + '/img/photos/coach2.jpg'
    ],
    'footer': [
        settings.STATICFILES_DIRS[0] + '/img/photos/footer1.jpg',
        settings.STATICFILES_DIRS[0] + '/img/photos/footer2.jpg'
    ]
}


def get_random_photo(section):
    if section in DEFAULT_BACKGROUND_PHOTOS:
        photos = DEFAULT_BACKGROUND_PHOTOS[section]
        return UploadedFile(
            open(photos[random.randint(0, len(photos) - 1)], 'rb')
        )
    return None


def get_default_eventpage_data():
    return [
        {
            'name': 'about',
            'is_public': True,
            'background': get_random_photo('about'),
            'template': 'default/about.html'
        },
        {
            'name': 'values',
            'is_public': True,
            'template': 'default/values.html'
        },
        {
            'name': 'apply',
            'is_public': True,
            'background': get_random_photo('apply'),
            'template': 'default/apply.html'
        },
        {
            'name': 'faq',
            'is_public': True,
            'template': 'default/faq.html'
        },
        {
            'name': 'coach',
            'is_public': True,
            'background': get_random_photo('coach'),
            'template': 'default/coach.html'
        },
        {
            'name': 'partners',
            'is_public': True,
            'template': 'default/partners.html'
        },
        {
            'name': 'footer',
            'is_public': True,
            'background': get_random_photo('footer'),
            'template': 'default/footer.html'
        },
    ]


def get_default_menu():
    return [
        {'title': 'About', 'url': '#values'},
        {'title': 'Apply for a pass!', 'url': '#apply'},
        {'title': 'FAQ', 'url': '#faq'},
        {'title': 'Become a coach', 'url': '#coach'},
        {'title': 'Partners', 'url': '#partners'},
    ]
