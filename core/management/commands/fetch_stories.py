# -*- encoding: utf-8 -*-
from __future__ import unicode_literals, print_function

import requests
try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen
from xml.etree import ElementTree
from pyquery import PyQuery as pq

from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from core.models import Story


class Command(BaseCommand):
    help = 'Fetch Django Girls stories from our blog'

    def handle(self, *args, **options):

        rss_url = 'http://blog.djangogirls.org/rss'

        response = requests.get(rss_url)
        rss = ElementTree.fromstring(response.content)

        for post in rss.iter('item'):
            title = post.find('title').text
            if 'Your Django Story: Meet' in title:
                name = title.replace('Your Django Story: Meet ', '')

                if not Story.objects.filter(name=name).exists():
                    post_url = post.find('link').text
                    post = pq(post.find('description').text)
                    image_url = post('img').attr.src

                    if image_url:
                        story = Story(name=name, post_url=post_url)

                        img = NamedTemporaryFile(delete=True)
                        img.write(urlopen(image_url).read())
                        img.flush()

                        story.image.save(image_url.split('/')[-1], File(img))
                        story.save()

                        print('Story of %s has been fetched' % name)
