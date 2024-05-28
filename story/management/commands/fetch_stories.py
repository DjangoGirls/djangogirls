from urllib.error import HTTPError, URLError
from xml.etree import ElementTree

import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.management.base import BaseCommand
from pyquery import PyQuery as pq  # noqa: N813

from story.models import Story

try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen


class Command(BaseCommand):
    help = "Fetch Django Girls stories from our blog"

    def handle(self, *args, **options):
        rss_url = "http://blog.djangogirls.org/rss"

        response = requests.get(rss_url)
        rss = ElementTree.fromstring(response.content)

        for post in rss.iter("item"):
            title = post.find("title").text
            if "Your Django Story: Meet" in title:
                name = title.replace("Your Django Story: Meet ", "")
                is_story = True
            else:
                name = title
                is_story = False

            if not Story.objects.filter(name=name).exists():
                post_url = post.find("link").text
                _post = pq(post.find("description").text)
                image_url = _post("img").attr.src
                story = Story(name=name, post_url=post_url, content=_post, is_story=is_story)

                if image_url:
                    try:
                        with NamedTemporaryFile(delete=True) as img:
                            img.write(urlopen(image_url).read())
                            img.flush()
                            story.image.save(image_url.split("/")[-1], File(img))
                    except HTTPError as e:
                        print(f"HTTP error when fetching image from {image_url}: {e.code} {e.reason}")
                    except URLError as e:
                        print(f"URL error when fetching image from {image_url}: {e.reason}")
                    except Exception as e:
                        print(f"Unexpected error when fetching image from {image_url}: {e}")

                story.save()

                if is_story:
                    print(f"Story of {name} has been fetched")
                else:
                    print(f'Blogpost "{name}" has been fetched')
